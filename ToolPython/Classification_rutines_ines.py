#I want with this document to explore the accuraccies after validation of
#all the imagery over the Time
#240158
###   --folder_path   /home/user/Documents/TESISMASTER/VECTOR/Training_data_ImageryST

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
import matplotlib.pyplot as plt
import lulc
import Active_learning as al
import os
import numpy as np
import pandas as pd
import argparse

#parsing

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", help = "Name of the folder with the shapefiles")
    args = parser.parse_args()
    print(args.folder_path)

list_folder_path = [os.path.join(args.folder_path, i) for i in os.listdir(args.folder_path)]
list_folder_path.sort()
print(list_folder_path)

#name of the files

#create object for classication
for i in list_folder_path:
    name = i.split("/")[-1].split("_")[1]
    #preparing dataset for mdelling
    dataset = al.import_data(os.path.join(i,"training_samples8_rf_w.shp"))
    #pereparing dataset for testing
    dataset_testing = al.import_data(os.path.join(i,"BD_REF_HUGO2.shp"))
    #spliting data in training and validation
    random = al.random_selection(dataset,prob = 0.7, pivot= "CLASS_NAME")
    (train,valid) = random.stratified_random_selection()
    X_train = train["data"].iloc[:,1:14].values
    y_train = train["data"]["CLASS_NAME"].values
    X_valid = valid["data"].iloc[:,1:14].values
    y_valid = valid["data"]["CLASS_NAME"].values
    #testing data 1 external
    X_test = dataset_testing["data"].iloc[:,1:14].values
    y_test = dataset_testing["data"]["CLASS_NAME"].values
    classifier= svm.SVC(C=4, kernel = 'rbf',gamma= 0.25)
    #classifier = KNeighborsClassifier(n_neighbors = 10)
    #training
    classifier.fit(X_train, y_train)
    #classifying validation and testing data
    result_valid = classifier.predict(X_valid)
    result_test = classifier.predict(X_test)
    df_0 = pd.DataFrame(result_test)
    df_1 = pd.concat([dataset_testing["data"]["CLASS_NAME"],df_0], axis = 1,ignore_index =True)
    df_1.columns = ["CLASS_NAME",name]
    print(df_1.head(4))
    #creating a copy of dataset
    dataset_output  = {}
    dataset_output = {
        "coordinates":dataset_testing["coordinates"],
        "data":df_1,
        "proj":dataset_testing["proj"]
    }
    path_out = os.path.join(i,'Prediction_' + name + ".shp")
    al.write_shapefile(dataset_output, path_out)
    print(f"done {i}")
