#!/usr/bin/env python

import pandas_datareader as pdr
import pandas as pd
import numpy as np
import os
import math
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout, BatchNormalization
from credentials.token import key

class TechnicalPricePrediction():
    def __init__(self, ticker):
        self.__ticker = ticker
        self.__time_step = 60 # you may want to change this
        self.__data = self.__get_data()
        self.__scaled_data, self.__scale = self.__scale_data()

    def __get_data(self):
        ticker = self.__ticker
        path = f'datasets/{ticker}.csv'
        if(not os.path.isfile(path)):
            print("Made an API call")
            df = pdr.get_data_tiingo(ticker, api_key=key)
            df.to_csv(path);
            print("Done reading")
        df = pd.read_csv(path)
        df_price = df.reset_index()['open']
        return df_price


    def __scale_data(self, feature_range=(0,1)):
        scale = MinMaxScaler(feature_range = feature_range)
        df = scale.fit_transform(np.array(self.__data).reshape(-1,1)) # (-1,1) figure out first dimension
        return df, scale


    def __load_dataset(self, data, time_back=60):
        time_back = self.__time_step
        l = len(data)
        X = []
        Y = []
        for i in range(l-time_back):
            X.append(data[i:i+time_back])
            Y.append(data[i+time_back])
        X = np.array(X)
        Y = np.array(Y)
        return X, Y

    def __define_model(self, ip_shape=None):
        model = Sequential()
        model.add(LSTM(25, return_sequences=True, input_shape=ip_shape))
        model.add(Dropout(0.2))
        
        model.add(LSTM(50, return_sequences=True))
        model.add(Dropout(0.2))
        
        model.add(LSTM(75))
        model.add(Dropout(0.2))
        
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model


    def __train(self):
        time_step = self.__time_step
        path = f'models/{self.__ticker}.h5'
        if os.path.exists(path):
            model = load_model(path)
            return model

        df_scaled, scale = self.__scaled_data, self.__scale
        percent_80 = int(len(df_scaled) * 0.80)
        train_X, train_Y = self.__load_dataset(df_scaled[:percent_80]);
        validation_X, validation_Y = self.__load_dataset(df_scaled[percent_80:])
        model = self.__define_model(train_X.shape[1:]) 
        model.fit(train_X, train_Y, validation_data=(validation_X, validation_Y), epochs=100, batch_size=32, verbose=1)
        model.save(f'models/{self.__ticker}.h5')

        return model


    def predict(self, lazy=False):
        model = self.__train()

        df = None
        if lazy:
            df = pd.read_csv(f'datasets/{self.__ticker}.csv')
        else:
            df = pdr.get_data_tiingo(self.__ticker, api_key=key)
            
        df_price = df.reset_index()['open']

        df_price = self.__scale.transform(np.array(df_price).reshape(-1,1))
        time_step = self.__time_step

        l = len(df_price) - time_step # 60 => time_step
        op_X = self.__load_dataset(df_price)
        op_X = []
        x = []
        for i in range(time_step):
            x.append(df_price[l-i-1])
        op_X.append(x)
        op_X = np.array(op_X)
        op_predict = model.predict(op_X)
        op_Y = self.__scale.inverse_transform(op_predict)
        return op_Y[0][0]

test = TechnicalPricePrediction('TTWO')
print("\nPrediction:",test.predict())