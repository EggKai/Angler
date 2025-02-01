import joblib
import pandas as pd

ensemble = joblib.load(r'models/AnglerLLM/ensemble_model.pkl')
vectorizer = joblib.load(r'models/AnglerLLM/tfidf_vectorizer.pkl')

def LLM_probablity(text:str):
    # Step 2.3: Transform the text into TF-IDF features
    dataframe = pd.DataFrame({
        'id': ['custom_article'],
        'text': [text]})
    X_test_tfidf = vectorizer.transform(dataframe['text'])

    predictions = ensemble.predict_proba(X_test_tfidf)[:, 1]  # Probability of being AI-generated
    return round(predictions[0]*100,1)
