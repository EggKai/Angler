
import pandas as pd
import joblib

spam_classifier = joblib.load(r'models/SpamAssassin/spam_classifier.pkl')
def predict_spam_probability(emails : str):
    return round(spam_classifier.predict_proba(pd.Series(emails))[0][0] * 100, 1)

if __name__ == "__main__":
    emails = ['Dear user, you have won a lottery of $1000000. Please click on the link to claim your prize.',
              'Dear user, your account has been locked. Please click on the link to unlock your account.']
    predict_spam_probability(emails)