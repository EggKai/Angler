import pickle
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from .URLFeatureExtraction import feature_extraction
from .external import check_phishing_phishtank, extract_domain, extractUrls
with open('models/AnglerUrl/xgboost_url_model.pkl', 'rb') as file: # Load the trained model
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
    return prediction == 1 
def checkUrls(text, urls):
    if not (all_urls:=[url for url in extract_domain(extractUrls(text))+urls if url != '://']):
        return None
    with ThreadPoolExecutor() as executor:
        results = dict(zip(all_urls, executor.map(check_phishing_phishtank, all_urls)))
    return {result['url']: result["is_phishing"] if result['found'] else predict_url(result['url']) for result in results}
if __name__ == "__main__":
    test_url = "https://www.quicksharebd.xyz/2025/01/solo-leveling-season-2-arise-from-shadow.html"
    result = predict_url(test_url)
    print(f"The URL '{test_url}' is classified as: {'Malicious' if result else 'Legitimate'}")
