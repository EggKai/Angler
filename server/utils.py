import html
from models import checkUrls
# from models import probability_of_spam, apply_preprocess_text
import random

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
        "Spam" : random.randint(1,99),
        "Phishing" : random.randint(50,99),
        "LLM" : random.randint(90,100),
        "urls" : checkUrls(text, urls),
        "Code" : "Safe",
        "Executables" : "Malicious"
    }