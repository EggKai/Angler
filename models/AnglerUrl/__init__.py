import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
from .external import check_phishingUrl
phishingUrl_classifier = joblib.load('models/AnglerUrl/phishing_url_detection_model.pkl')

def phishingUrlLocal(url: str):
    pass

if __name__ == "__main__":
    print(f"probability_of_phishing: {phishingUrlLocal('https://123movies.com')}")