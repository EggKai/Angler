import re
import requests
import ipaddress
import whois
from urllib.parse import urlparse, unquote
from datetime import datetime, timedelta


# Constants for URL shortening services
SHORTENING_SERVICES = (
    r"(bit\.ly|73\.nu|cutt\.ly|dub\.sh|foxly\.me|han\.gl|is\.gd|kurzlinks\.de|kutt\.it|"
    r"reduced\.to|catbox\.moe|urlzs\.com|shorturl\.at|spoo\.me|tinu\.be|switchy\.io|"
    r"t\.ly|urlr\.me|v\.gd|yaso\.su|vo\.la|ishortn\.ink|pastebin\.com)"
)


def having_ip(url):
    """Check if the URL contains an IP address."""
    try:
        hostname = urlparse(url).hostname
        ipaddress.ip_address(hostname)
        return 1  # phishing
    except ValueError:
        return 0  # legitimate


def get_url_length(url):
    """Check if the length of the URL is greater than or equal to 54 characters."""
    return 1 if len(url) >= 54 else 0


def http_in_domain(url):
    """Check if the domain part of the URL contains 'https'."""
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else 0


def is_tiny_url(url):
    """Check if the URL is from a known URL shortening service."""
    match = re.search(SHORTENING_SERVICES, url)
    return 1 if match else 0


def has_prefix_suffix(url):
    """Check if the domain part of the URL contains a '-' (prefix/suffix)."""
    return 1 if '-' in urlparse(url).netloc else 0


def check_no_extension(url):
    """Check if the URL does not end with an extension (e.g., .exe, .zip)."""
    parsed_url = urlparse(url)
    path = parsed_url.path
    decoded_path = unquote(path)
    return 1 if '.' in decoded_path.split('/')[-1] else 0


def count_urls_in_webpage(url):
    """Check if a webpage contains more than 3 URLs."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
        urls = re.findall(r'https?://[^\s"]+', content)
        return 0 if len(urls) > 3 else 1
    except requests.RequestException:
        return 0  # Error or no URLs


def check_redirection_to_another_domain(url):
    """Check if the URL redirects to another domain."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        final_url = response.url
        initial_domain = urlparse(url).netloc
        final_domain = urlparse(final_url).netloc
        return 1 if initial_domain != final_domain else 0
    except requests.RequestException:
        return 0  # Error case


def check_domain_registration_date(url):
    """Check if the domain was registered within the last 6 months."""
    try:
        domain_name = urlparse(url).netloc
        whois_info = whois.whois(domain_name)
        registration_date = whois_info.creation_date
        if isinstance(registration_date, list):
            registration_date = registration_date[0]
        if isinstance(registration_date, str):
            registration_date = datetime.strptime(
                registration_date.replace('th', '').replace('st', '').replace('nd', '').replace('rd', ''),
                '%d %B %Y at %H:%M:%S.%f'
            )
        if registration_date:
            six_months_ago = datetime.now() - timedelta(days=6 * 30)
            return 1 if registration_date > six_months_ago else 0
        return 1  # Error case
    except Exception:
        return 1  # Error case


def domain_age(domain_name):
    """Calculate the age of the domain based on WHOIS data."""
    try:
        creation_date = domain_name.creation_date
        expiration_date = domain_name.expiration_date
        if isinstance(creation_date, str) or isinstance(expiration_date, str):
            try:
                creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            except:
                return 1  # Error case
        if not expiration_date or not creation_date:
            return 1
        age_of_domain = abs((expiration_date - creation_date).days)
        return 1 if age_of_domain / 30 < 6 else 0
    except:
        return 1  # Error case


def feature_extraction(url, verbose=False):
    """Extract features from a URL for phishing detection."""
    features = [url]
    # IP address presence
    ip = having_ip(url)
    features.append(ip)
    features.append(get_url_length(url))# URL length
    features.append(http_in_domain(url)) # HTTPS in domain
    features.append(is_tiny_url(url))# TinyURL shortening service
    features.append(has_prefix_suffix(url))# Prefix/Suffix in domain
    
    if ip == 0: # Domain registration check if the URL does not have an IP
        features.append(check_domain_registration_date(url))
    else:
        features.append(0)  # No registration date check for IP-based URLs
    features.append(check_no_extension(url))# Extension check
    features.append(count_urls_in_webpage(url))# Count of URLs in webpage
    features.append(check_redirection_to_another_domain(url))# Redirection to another domain
    
    if verbose:
        print(features)
    return features[1:]  # Return features excluding the URL


FEATURE_NAMES = [ # Define the feature names for the extracted data
    'Domain', 'Have_IP', 'URL_Length', 'https_Domain', 'TinyURL', 'Prefix/Suffix',
    'Domain_Age', 'Extension', 'Check_Depth', 'Redirect_Diff_Domain'
]
