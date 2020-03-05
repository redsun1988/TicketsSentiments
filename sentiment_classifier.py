__author__ = 'xead'
from sklearn.externals import joblib
import os

class SentimentClassifier(object):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))	
        self.model = joblib.load(path + "\sentimentClassifier.pkl")
        self.classes_dict = {0: "bad subject", 1: "good subject", -1: "prediction error"}

    def predict_text(self, text):
        try:
            return self.model.predict([text])[0]
        except:
            return -1   