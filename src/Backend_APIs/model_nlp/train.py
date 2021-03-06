import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_log_error
from sklearn.linear_model import LogisticRegression
import sys
import os
from model_nlp import preprocess
# from model_nlp.preprocess import *
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def classification_metrics(y_pred, y_test):
    acc = round(accuracy_score(y_test, y_pred),2)
    prec = round(precision_score(y_test, y_pred),2)
    rec = round(recall_score(y_test, y_pred),2)
    f1 = round(f1_score(y_test, y_pred), 2)
    return acc, prec, rec, f1


def build_model(train_data):
    X_train, X_test, y_train, y_test = preprocess.data_set_split(train_data)
    X_train = X_train.apply(preprocess.text_normalize)
    X_test = X_test.apply(preprocess.text_normalize)
    X_train_new = preprocess.vectorizer(X_train)
    X_test_new = preprocess.vectorizer(X_test)

    log_reg = LogisticRegression()
    log_reg.fit(X_train_new, y_train)
    joblib.dump(log_reg, "src/Backend_APIs/model_nlp/models/model.joblib", compress=0, protocol=None, cache_size=None)
    
    y_pred = log_reg.predict(X_test_new)
    
    accurancy, precision, recall, f1_score = classification_metrics(y_test, y_pred)
    return {'Accurancy': accurancy,
            'Precision': precision,
            'Recall': recall,
            'F1 score': f1_score}