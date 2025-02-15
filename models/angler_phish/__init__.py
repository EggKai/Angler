
import pandas as pd
import joblib

phishing_classifier = joblib.load(r'models/angler_phish/phishing_classifier.pkl')
def predict_phishing_probability(emails, verbose:bool=False):
    if verbose:
        print(phishing_classifier.predict_proba(pd.Series(emails))[0][1])
    return round(phishing_classifier.predict_proba(pd.Series(emails))[0][1] * 100, 1)

if __name__ == "__main__":
    emails = ['disc uniformitarian sex lang dick hudson observ u use aughter voc thoughtprovok sure fair attribut son treat like senior rel one thing nt normal use brother way aughter hard imagin natur class compris senior rel exclud brother anoth seem differ imagin distinct seem senior rel term use wider varieti context e g call distanc get someon attent henc begin utter wherea seem natur utter like ye son hand son one like son son help although perhap latter one complet imposs alexi mr']
    predict_phishing_probability(emails)