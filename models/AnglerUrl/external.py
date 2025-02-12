import requests, urllib.parse
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import urlextract, warnings
from functools import lru_cache

API_URL = "https://checkurl.phishtank.com/checkurl/"

@lru_cache(maxsize=50)  # Makes sure redundent calls are made faster
def check_phishing_phishtank(url_to_check, app_key=None, *, verbose: bool = False):
    """
    Checks if a URL is a known phishing site using the PhishTank API with a POST request.
    The PhishTank service allows users to check URLs for phishing activity.

    Parameters:
    ----------
    url_to_check : str
        The URL that you want to check for phishing.
    app_key : str, optional
        PhishTank application key allows for higher request limits (optional)

    Returns:
    -------
    dict
        A dictionary containing the result of the phishing check. The keys
        in the dictionary are:
        - 'url': The URL that was checked (str)
        - 'is_phishing': whether the URL is a phishing site (bool|None)
        - 'found': whether the url was found by the site (bool)

    Raises:
    ------
    requests.exceptions.RequestException
        If there is an issue with making the HTTP request to the PhishTank API or any network error.
    ValueError
        If the URL is not valid or the response format is unexpected.
    """
    encoded_url = urllib.parse.quote(url_to_check)
    request_data = {
        "url": encoded_url,
    }
    if app_key:
        request_data["app_key"] = app_key
    headers = {
        "User-Agent": "phishtank/Angler"  # Replace with your username or app name
    }
    try:
        response = requests.post(API_URL, data=request_data, headers=headers)
        if verbose:
            print("Raw response content:", response.text)
        response.raise_for_status()  # Raise exception for HTTP errors (4xx, 5xx)
        if response.status_code == 200:
            try:  # Parse XML response
                tree = ET.ElementTree(ET.fromstring(response.text))
                root = tree.getroot()
                errortext = root.find(
                    ".//errortext"
                )  # Extract the error text if there is one
                if errortext is not None:
                    raise ValueError(f"API Error: {errortext.text}")
                in_database = root.find(
                    ".//in_database"
                )  # Check if the URL is in the PhishTank database as phishing
                if in_database is not None and in_database.text == "true":
                    if (is_phishing := root.find(".//verified")) is not None:
                        return {
                            "url": url_to_check,
                            "is_phishing": is_phishing == "false",
                            "found": True,
                        }
            except ValueError:
                warnings.warn("The response from PhishTank is not in XML format.")
        else:
            warnings.warn(
                f"Error: Received non-200 status code {response.status_code}."
            )
    except requests.exceptions.RequestException as e:
        warnings.warn(
            f"Error in API request: {e}; {url_to_check}"
        )  # Catch network-related errors or other HTTP exceptions
    return {
        "url": url_to_check,
        "is_phishing": None,
        "found": False,
    }
    
def extractUrls(text:str, urlExtractor:urlextract.URLExtract=urlextract.URLExtract()) -> list:
    return urlExtractor.find_urls(text)

def extract_domain(urls:list) -> set:
    return set(f"{urlparse(url).scheme}://{urlparse(url).netloc}" for url in urls if urlparse(url).netloc)

def is_downloadable(url):
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get("Content-Type", "").lower()
        content_disposition = response.headers.get("Content-Disposition", "")

        # Check for Content-Disposition with filename
        if "attachment" in content_disposition.lower() or "filename=" in content_disposition:
            return True

        # Check for content types that are often downloadable
        return content_type in [
            "application/octet-stream",
            "application/zip",
            "application/pdf",
            "application/x-msdownload",
            "application/vnd.ms-excel",
            "application/vnd.ms-powerpoint",
            "application/msword"
            ]
    except requests.RequestException:
        return False


if __name__ == "__main__":
    # assert not check_phishing_phishtank("https://www.dbs.com.sg/index/default.page")[
    #     "is_phishing"
    # ], "This DBS link is real"
    print(is_downloadable("https://git.abyssaltar.com/water/"))