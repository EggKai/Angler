import html
from models import checkUrls, LLM_probablity, predict_phishing_probability, predict_spam_probability
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
        "Spam" : predict_spam_probability(text),
        "Phishing" : predict_phishing_probability(text),
        "LLM" : LLM_probablity(text),
        "urls" : checkUrls(text, urls),
        "Code" : "Safe",
        "Executables" : "Safe"
    }