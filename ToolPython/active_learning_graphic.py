##removing data and evaluating accuraccy
#since I want a backup of the process I store and recall agin the Shapefile
#====================================
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import fetch_mldata
from sklearn.preprocessing import MinMaxScaler  #StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import os
import Active_learning as al
import numpy as np
from osgeo import gdal, ogr
import pandas as pd

#====================================

file_imput = "/home/user/Documents/TESISMASTER/VECTOR/Training_data_bands/IM_20170927/training_samples3_w_rf.shp"

dataset1 = al.import_data(file_imput)

intervals = 20
threshold = np.arange(0.1,0.7,0.01).tolist()
g = []
for i in threshold:
    id = np.where(dataset1["data"]["weights"].values > i)[0]
    #quering with the threshold criterium
    n_data = {}
    n_data["data"] = dataset1["data"].loc[id]
    n_data["data"] = n_data["data"].reset_index()
    del n_data["data"]['index']
    #coordinates
    n_data["coordinates"] = dataset1["coordinates"].loc[id]
    n_data["coordinates"] = n_data["coordinates"].reset_index()
    del n_data["coordinates"]['index']
    n_data["proj"] = dataset1["proj"]
    #new random selection test and training
    randoma = al.random_selection(n_data,prob = 0.7, pivot= "CLASS_NAME")
    (train_q, test_q) = randoma.stratified_random_selection()
    X_train = train_q["data"].iloc[:,1:].values
    y_train = train_q["data"]["CLASS_NAME"].values
    X_test = test_q["data"].iloc[:,1:].values
    y_test = test_q["data"]["CLASS_NAME"].values
    print(X_train)
    #RandomForestClassifier
    classifier = RandomForestClassifier(n_estimators=500)
    classifier.fit(X_train,y_train)
    result = classifier.predict(X_test)
    print(f'done {i}')
    print('Overal Accuracy: ', accuracy_score(result, y_test))
    g.append(accuracy_score(result, y_test))
    n_data = None

print(g)
