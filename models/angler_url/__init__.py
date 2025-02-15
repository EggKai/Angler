import pickle
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from .URLFeatureExtraction import feature_extraction
from .external import check_phishing_phishtank, extract_domain, extractUrls, is_downloadable
with open('models/angler_url/xgboost_url_model.pkl', 'rb') as file: # Load the trained model
    loaded_model = pickle.load(file)
def predict_url(url:str) -> bool :
    """Predict if a URL is malicious or legitimate.
    Args:
        url (str): The URL to classify.
    Returns:
        bool: True: 'Malicious' or False: 'Legitimate'.
    """
    features = feature_extraction(url) # Extract features from the URL
    features = np.array(features).reshape(1, -1)  # Reshape for the model
    prediction = loaded_model.predict(features)[0] # Make a prediction
    return bool(prediction) #convert numpy boolean value to python boolean value

def checkUrls(text:str, urls:str) -> dict:
    all_urls = extractUrls(text)+urls
    if not (all_domains:=list(filter(lambda url: url != '://', extract_domain(all_urls)))):
        return None
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(check_phishing_phishtank, all_domains))
    return {
        domain['url']: domain["is_phishing"] if domain['found'] else next(
            (predict_url(url) for url in all_urls if url.startswith(domain['url'])), None
        ) for domain in results
    }

if __name__ == "__main__":
    test_url = "https://www.quicksharebd.xyz/2025/01/solo-leveling-season-2-arise-from-shadow.html"
    another_url ="https://ctrack.feverup.com/ls/click?upn=u001.KYa3IGmNOpE6PwzGuZi8uMyeFNJJoHmX4191VOSLXlIznl3Ew-2BwmypUdsEDD-2FYc5MlHcd933oPDTOv6lC9d2-2Fpa7lbMLf4eJdbwbUYl7IimCZMJ18XGpv269xCESRogmMg-2FKGreIRtmi-2BtH1ChqRJ0wF5S7807WFfY2O8eMSOm6GHZn1n3mVIO8KD-2FwUdq6A9JPGknyTuIzR-2Fq9NMcuo1fj2JBMZr28xcL61Er4UqRE-3DgCBs_9LyoeWowCu06l4yit2-2Fz0npiRtDOxrcJkvAeaIydGbAuX4JsqXtI0YgBetrhPzufLTmRc0jegoLwsu9KBlmdPRZzM6e-2FpLxApJPgEEGXKaGHtnVYAgI4-2FbmgNUxSB5NDk0SVKbi4oQdkgtG3syQJ0ub7uhlLpV-2BhvETVG-2BFFMF66v16qX2WV9DdQCg4fvD-2FCiNM0yZ9gtorGbskoe-2Fh4a2ws9na2ElgearPDNdrvqgRn4x2DsmVmmnml57CCNSja4XqExEpdRv1jWcvYDXdA1ZEOKCw7N-2B765So2pLAIeNWkLkeZWIDj6g76mqZzZONwFFbeCahBWq2YD9Kq92rukzhUrjV4cN-2BK3g8WTSXzYa-2FbagGrvpySFwF4mntTlQxPyNn1JRQyLLJW7uzZRP5foDar9LR-2BJx5Swoh3GDmgbEDpUBto4N1qS5aFp2A5ltj2Tw76xXvC2LfQW23lr6D663uZKlih71tkjinAwOZUJzDNri6huWYtWVOTJAfT-2FsWovO-2FrsxDS-2F-2BVshhv-2BaR5s1g-3D-3D"
    result = predict_url(another_url)
    print(f"The URL is classified as: {'Malicious' if result else 'Legitimate'}")