import html
from itertools import zip_longest
from typing import List
from image_processing import process_images, read_qr_codes, DownloadFile
from models import checkUrls, LLM_probablity, predict_phishing_probability, predict_spam_probability

def sanitize_content(content):
    """Sanitize the content to avoid XSS (HTML escaping)."""
    return html.escape(content)

def checkContent(text:str, urls:List[str], imgUrls:List[str], attachmentPaths):
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
        for file, text in zip_longest(temp_files, process_images(temp_files), fillvalue=None):
            if qr_data:=read_qr_codes(file):
                urls+=qr_data
            if text:
                text+= text

    return { 
        "Spam" : predict_spam_probability(text),
        "Phishing" : predict_phishing_probability(text),
        "LLM" : LLM_probablity(text),
        "urls" : checkUrls(text, urls),
        "attachments" : {}
    }