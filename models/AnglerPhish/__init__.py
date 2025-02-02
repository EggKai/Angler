
import pandas as pd
import joblib
# pipeline_sgd = Pipeline(steps=[
#     ('clean', email_to_clean_text()),
#     ('tfidf', TfidfVectorizer(stop_words='english')),
#     ('model', CalibratedClassifierCV(SGDClassifier(loss='log_loss', random_state=0), method='isotonic'))
# ])

phishing_classifier = joblib.load(r'models/AnglerPhish/phishing_classifier.pkl')
def predict_phishing_probability(emails):
    prob = round(phishing_classifier.predict_proba(pd.Series(emails))[0][0] * 100, 2)
    print('The probability of phishing is {prob} %'.format(prob=prob))
    return prob
