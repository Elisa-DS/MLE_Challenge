#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 00:47:28 2022

@author: echimenton
"""

# imports
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.feature_selection import SelectKBest, mutual_info_regression

import joblib


def runTraining():
    
    '''
    *******************************
                TRAINING
    *******************************   
    '''
    
    precio_leche_pp_pib = joblib.load('./serialization/trainingDataSet.pkl') 
    
    X = precio_leche_pp_pib.drop(['Precio_leche'], axis = 1)
    y = precio_leche_pp_pib['Precio_leche']
    
    # generate random data-set
    np.random.seed(0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    pipe = Pipeline([('scale', StandardScaler()),
                     ('selector', SelectKBest(mutual_info_regression)),
                     ('poly', PolynomialFeatures()),
                     ('model', Ridge())])
    k=[3, 4, 5, 6, 7, 10]
    alpha=[1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    poly = [1, 2, 3, 5, 7]
    grid = GridSearchCV(estimator = pipe,
                        param_grid = dict(selector__k=k,
                                          poly__degree=poly,
                                          model__alpha=alpha),
                        cv = 3,
                        scoring = 'r2')
    grid.fit(X_train, y_train)
    
    
    '''
    *******************************
            SERIALIZATION
    *******************************            
    '''
    
    # Save Model
    joblib.dump(grid, './serialization/linearRegression.pkl')
    print("Linear Regression Model Saved")
    
    # Save features from training
    lr_columns = list(X_train.columns)
    joblib.dump(lr_columns, './serialization/lr_columns.pkl')
    print("Regression Model Colums Saved")