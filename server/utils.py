import html
from models import checkUrls
# from models import probability_of_spam, apply_preprocess_text

def sanitize_content(content):
    """Sanitize the content to avoid XSS (HTML escaping)."""
    return html.escape(content)

def checkContent(text, urls, imgUrls):
    """
    Check text 
        -> Spam
        -> Phishing
        -> LLM generated
    Check images -> Text
        -> Phishing
    Check URLs
        -> check domain validity
    Check Attachments
        -> Malicious or not
    """
    
    
    return { #placeholder numbers
        "Spam" : 40.2,
        "Phishing" : 50.6,
        "LLM" : 90.8,
        "urls" : checkUrls(text, urls),
        "Code" : "Safe",
        "Executables" : "Malicious"
    }