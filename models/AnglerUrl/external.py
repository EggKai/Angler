import requests, urllib.parse
import xml.etree.ElementTree as ET
API_URL = "https://checkurl.phishtank.com/checkurl/"

def check_phishing_phishtank(url_to_check, app_key=None, *, verbose:bool=False):
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
        'url': encoded_url,
    }
    if app_key:
        request_data['app_key'] = app_key
    headers = {
        'User-Agent': 'phishtank/Angler'  # Replace with your username or app name
    }
    try:
        response = requests.post(API_URL, data=request_data, headers=headers)
        if verbose: print("Raw response content:", response.text)
        response.raise_for_status() # Raise exception for HTTP errors (4xx, 5xx)
        if response.status_code == 200:
            try: # Parse XML response
                tree = ET.ElementTree(ET.fromstring(response.text))
                root = tree.getroot()
                errortext = root.find('.//errortext') # Extract the error text if there is one
                if errortext is not None:
                    raise ValueError(f"API Error: {errortext.text}")
                in_database = root.find('.//in_database') # Check if the URL is in the PhishTank database as phishing
                if in_database is not None and in_database.text == 'true':
                    if (is_phishing:=root.find(".//verified")) is not None:
                        return {
                            'url': url_to_check,
                            'is_phishing': is_phishing == 'false',
                            'found': True
                        }
                return {
                    'url': url_to_check,
                    'is_phishing': None,
                    'found': False
                }
            except ValueError:
                raise ValueError("The response from PhishTank is not in XML format.")
        else:
            raise requests.exceptions.RequestException(f"Error: Received non-200 status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Error in API request: {e}") # Catch network-related errors or other HTTP exceptions


if __name__ == "__main__":
    assert not check_phishing_phishtank("https://www.dbs.com.sg/index/default.page")['is_phishing'], "This DBS link is real"