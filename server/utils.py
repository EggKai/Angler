import html
from typing import List
from image_processing import perform_ocr, read_qr_codes, DownloadFile
from models import checkUrls, LLM_probablity, predict_phishing_probability, predict_spam_probability
from functools import lru_cache

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
            for file in temp_files:
                qr_data=read_qr_codes(file)
                if qr_data:
                    urls+=qr_data
            
    with DownloadFile(imgUrls) as temp_files2:
        if temp_files2:
            for file in temp_files2:
                ocr_text = perform_ocr(file)
                if ocr_text:
                    text+= ocr_text
    return { 
        "Spam" : predict_spam_probability(text),
        "Phishing" : predict_phishing_probability(text),
        "LLM" : LLM_probablity(text),
        "urls" : checkUrls(text, urls),
    }
def verdict(checked_content: dict) -> bool:
    return bool(
        checked_content["Spam"] >= 96
        or checked_content["Phishing"] >= 84
        or checked_content["LLM"] >= 50
        or any(checked_content.get("urls", {}).values())
        or any(checked_content.get("attachments", {}).values())
    ) #stop it from typecasting np.True__
