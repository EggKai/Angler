import pandas as pd
import string
from bs4 import BeautifulSoup
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import re
import email
from sklearn.feature_extraction.text import CountVectorizer
import os 
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
stemmer = PorterStemmer()
vectorizer = CountVectorizer(stop_words='english')
lemmatizer = WordNetLemmatizer()
from sklearn.linear_model import SGDClassifier
import joblib

class email_to_clean_text(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None): 
        return self
    def transform(self, X):
        text_list = []
        for mail in X:
            b = email.message_from_string(mail)
            body = ""

            if b.is_multipart():
                for part in b.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))

                    # skip any text/plain (txt) attachments
                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        body = part.get_payload(decode=True)  # get body of email
                        break
            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
            else:
                body = b.get_payload(decode=True) # get body of email
            #####################################################
            soup = BeautifulSoup(body, "html.parser") #get text from body (HTML/text)
            text = soup.get_text().lower()
            #####################################################
            text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE) #remove links
            ####################################################
            text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text, flags=re.MULTILINE) #remove email addresses
            ####################################################
            text = text.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
            ####################################################
            text = ''.join([i for i in text if not i.isdigit()]) # remove digits
            ####################################################
            stop_words = stopwords.words('english')
            words_list = [w for w in text.split() if w not in stop_words] # remove stop words
            ####################################################
            words_list = [lemmatizer.lemmatize(w) for w in words_list] #lemmatization
            ####################################################
            words_list = [stemmer.stem(w) for w in words_list] #Stemming
            text_list.append(' '.join(words_list))
        return text_list
    
# pipeline_sgd = Pipeline(steps=[
#     ('clean', email_to_clean_text()),
#     ('tfidf', TfidfVectorizer(stop_words='english')),
#     ('model', CalibratedClassifierCV(SGDClassifier(loss='log_loss', random_state=0), method='isotonic'))
# ])

phishing_classifier = joblib.load(r"C:\Users\Admin\Documents\Work\SIT_WORK\SIT_work\INF1002-Programming_fundamentals\project\spam_classifier.pkl")
def predict_phishing_probability(emails):
    prob = round(phishing_classifier.predict_proba(pd.Series(emails))[0][0] * 100, 2)
    print('The probability of phishing is {prob} %'.format(prob=prob))
    return prob
if __name__ == "__main__":
    predict_phishing_probability('''From: "Mr. Ben Suleman" <bensul200''')