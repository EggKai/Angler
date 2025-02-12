import html
from typing import List
from image_processing import perform_ocr, read_qr_codes, DownloadFile
from models import checkUrls, LLM_probablity, predict_phishing_probability, predict_spam_probability

def sanitize_content(content):
    """Sanitize the content to avoid XSS (HTML escaping)."""
    return html.escape(content)

def checkContent(text:str, urls:List[str], imgUrls:List[str]):
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
    with DownloadFile(imgUrls) as temp_files:
        if temp_files:
            for file in temp_files.copy():
                qr_data=read_qr_codes(file)
                if qr_data:
                    urls+=qr_data
            
    with DownloadFile(imgUrls) as temp_files:
        if temp_files:
            for file in temp_files:
                ocr_text = perform_ocr(file)
                if ocr_text:
                    text+= ocr_text
    return { 
        "Spam" : predict_spam_probability(text),
        "Phishing" : predict_phishing_probability(text),
        "LLM" : LLM_probablity(text),
        "urls" : checkUrls(text, urls),
        "attachments" : {}
    }
def total_score():
    pass