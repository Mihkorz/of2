#!/usr/bin/python
import sys
import pickle
import numpy as np
import pandas as pd

from keras.models import model_from_json
    
def load_neural_network(file_from):
    """
    file_from - pickled Keras Sequantial with architecture and weights 
    """
    (nn_arch, nn_weights) = pickle.load(open(file_from, 'rb'))
    nn = model_from_json(nn_arch)
    nn.set_weights(nn_weights)
    
    return nn

def nn_predict(nn, to_predict, scaler, is_age=True):
    """
    nn - Keras Sequantial NN
    to_predict - np.array(s)
    is_age - if True then predict age, if False then predict gender
    
    return - age or gender
    """
    to_predict = scaler.transform(to_predict)
    mask = to_predict.shape == (len(to_predict), )
    
    to_predict = to_predict.reshape(1, len(to_predict)) if mask else to_predict
    
    return nn.predict(to_predict).ravel()[0].round() if mask                     else nn.predict(to_predict).ravel().round()


# Examples

samples = pd.read_csv('./'+str(sys.argv[1]))
scaler = pickle.load(open('./scaler_v2.pkl', 'rb'))
nn_gender = load_neural_network('./nn_gender_v2.insnn')
nn_age = load_neural_network('./nn_age_v2.insnn')

print(nn_predict(nn_age, samples.iloc[-1], scaler))
#print(nn_predict(nn_age, np.array(samples)[-1], scaler))
#print(nn_predict(nn_gender, samples.iloc[-1], scaler, is_age=False))
#print(nn_predict(nn_age, samples, scaler))
#print(nn_predict(nn_gender, samples, scaler, is_age=False))
#print(samples.columns.tolist())
