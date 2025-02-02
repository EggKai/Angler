
import pandas as pd
import joblib


# pipeline_sgd = Pipeline(steps=[
#     ('tfidf', TfidfVectorizer(stop_words='english')),
#     ('model', CalibratedClassifierCV(SGDClassifier(loss='log_loss', random_state=0), method='isotonic'))
# ])

spam_classifier = joblib.load(r'models/SpamAssassin/spam_classifier.pkl')
def predict_spam_probability(emails : str):
    prob = round(spam_classifier.predict_proba(pd.Series(emails))[0][0] * 100, 2)
    print('The probability of spam is {prob} %'.format(prob=prob))
    return prob

if __name__ == "__main__":
    emails = ['Dear user, you have won a lottery of $1000000. Please click on the link to claim your prize.',
              'Dear user, your account has been locked. Please click on the link to unlock your account.']
    predict_spam_probability(emails)