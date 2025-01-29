import html, urlextract
from models import check_phishing_phishtank
# from models import probability_of_spam, apply_preprocess_text
from urllib.parse import urlparse

def sanitize_content(content):
    """Sanitize the content to avoid XSS (HTML escaping)."""
    return html.escape(content)

def extractUrls(text:str, urlExtractor:urlextract.URLExtract=urlextract.URLExtract()):
    return urlExtractor.find_urls(text)

def checkContent(text, urls, imgUrls):
    def checkUrls(text, urls):
        def extract_domain(urls):
            return set(f"{urlparse(url).scheme}://{urlparse(url).netloc}" for url in urls)
        textUrls = extractUrls(text)
        if urls or textUrls:
            print("urls:", [check_phishing_phishtank(url) for url in list(extract_domain(textUrls))+list(extract_domain(urls)) if url != '://'])
    checkUrls(text, urls)