import pickle
import numpy as np
from .URLFeatureExtraction import feature_extraction
from .external import check_phishing_phishtank
with open('models/AnglerUrl/xgboost_url_model.pkl', 'rb') as file: # Load the trained model
    loaded_model = pickle.load(file)
def predict_url(url):
    """Predict if a URL is malicious or legitimate.
    Args:
        url (str): The URL to classify.
    Returns:
        bool: True: 'Malicious' or False: 'Legitimate'.
    """
    # Extract features from the URL
    features = feature_extraction(url)
    features = np.array(features).reshape(1, -1)  # Reshape for the model
    prediction = loaded_model.predict(features)[0] # Make a prediction
    return prediction == 1 
# Example usage
if __name__ == "__main__":
    test_url = "https://www.quicksharebd.xyz/2025/01/solo-leveling-season-2-arise-from-shadow.html"
    result = predict_url(test_url)
    print(f"The URL '{test_url}' is classified as: {'Malicious' if result else 'Legitimate'}")
