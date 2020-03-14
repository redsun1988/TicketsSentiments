__author__ = 'xead'
from sklearn.externals import joblib
import os
import numpy as np
import sys

class SentimentClassifier(object):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))	
        self.l1_classifier = joblib.load(path + "\l1_Classifier.pkl")
        self.l1_vectorizer = joblib.load(path + "\l1_vectorizer.pkl")
        self.l2_classifier = joblib.load(path + "\l2_Classifier.pkl")
        self.l2_vectorizer = joblib.load(path + "\l2_vectorizer.pkl")

    def predict_proba(self, text):
        try:
            l1_vect = self.l1_vectorizer.transform([text])
            l2_vect = self.l2_vectorizer.transform([text]).toarray()

            l_est = np.array([list([v]) for v in self.l1_classifier.predict(l1_vect)])
            l2_input = np.hstack((l2_vect, l_est))
            return float(np.max(self.l2_classifier.predict_proba(l2_input)))
        except:
            print(sys.exc_info())
            return -2   

    def predict_text(self, text):
        try:
            l1_vect = self.l1_vectorizer.transform([text])
            l2_vect = self.l2_vectorizer.transform([text]).toarray()

            l_est = np.array([list([v]) for v in self.l1_classifier.predict(l1_vect)])
            l2_input = np.hstack((l2_vect, l_est))

            return int(self.l2_classifier.predict(l2_input)[0])
        except:
            print(sys.exc_info())
            return -2   