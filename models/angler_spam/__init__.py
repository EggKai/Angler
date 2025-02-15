
import pandas as pd
import joblib

spam_classifier = joblib.load(r'models/angler_spam/spam_classifier.pkl')
def predict_spam_probability(emails:str, verbose:bool=False):
    if verbose:
        print(spam_classifier.predict_proba(pd.Series(emails))[0][1])
    return round(spam_classifier.predict_proba(pd.Series(emails))[0][0] * 100, 1)

if __name__ == "__main__":
    emails = ['Need a mortgage? Reply to arrange a call with a specialist and get a quote', ]
    predict_spam_probability(emails)