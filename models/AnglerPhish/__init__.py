
import pandas as pd
import joblib

phishing_classifier = joblib.load(r'models/AnglerPhish/phishing_classifier.pkl')
def predict_phishing_probability(emails):
    return round(phishing_classifier.predict_proba(pd.Series(emails))[0][0] * 100, 1)
