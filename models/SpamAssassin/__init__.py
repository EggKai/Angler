import re
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import FunctionTransformer
import pandas as pd
import joblib

def preprocess_text(text):
    # Remove hyperlinks
    text = re.sub(r'http\S+', '', text)
    # Remove punctuations
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def apply_preprocess_text(data):
    return data.apply(preprocess_text)

pipeline_sgd = Pipeline(steps=[
    ('text_preprocessing', FunctionTransformer(apply_preprocess_text)),  # Preprocessing
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('model', CalibratedClassifierCV(SGDClassifier(loss='log', random_state=0), method='isotonic'))
])
phishing_classifier = joblib.load('models/SpamAssassin/phishing_classifier.pkl')

def probability_of_spam(texts: str) -> float:
    text = pd.Series([texts])  #Pandas Series
    return phishing_classifier.predict_proba(text)[0][0] * 100 # Probability of class 1 (Phishing)

if __name__ == "__main__":
    print(f"probability of spam: {probability_of_spam('Send me your bank details to claim your prize!')}")