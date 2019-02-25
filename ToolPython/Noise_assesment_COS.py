#I want with this document to explore the accuraccies after validation of
#all the imagery over the Time
#240158
###   --folder_path  /home/user/Documents/TESISMASTER/VECTOR/Noise/Noise_6_classes/shapefiles

###  --test_shapefile /home/user/Documents/TESISMASTER/VECTOR/Training_data_ImageryST/IM_20170729/test_samples11.shp


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
    parser.add_argument("--test_shapefile", help = "Path of the test shapefile")
    args = parser.parse_args()
    print(f'processing {args.folder_path}')
    print(f'processing {args.test_shapefile}')

list_folder_path = [os.path.join(args.folder_path, i) for i in os.listdir(args.folder_path) if i.endswith("shp")]
list_folder_path.sort()
print(list_folder_path)

#create object for classication
for i in list_folder_path:
    #preparing dataset for mdelling
    dataset = al.import_data(i)
    #pereparing dataset for testing
    dataset_test = al.import_data(args.test_shapefile)
    row, col = dataset["data"].shape
    #creating file where I will store results of predicion of traning and testing of validation and testing
    file_val = os.path.join('/home/user/Documents/TESISMASTER/VECTOR/Noise/Noise_6_classes/Results',"validation_SVM_" + i.split(".")[0][-8:] + ".txt")
    f= open(file_val,"w+")
    #validation random selection cross validation
    for j in range(0,40):
        #spliting data in training and validation
        random = al.random_selection(dataset,prob = 0.7, pivot= "CLASS_NAME")
        (train,valid) = random.stratified_random_selection()
        X_train = train["data"].iloc[:,1:14].values
        y_train = train["data"]["CLASS_NAME"].values
        X_valid = valid["data"].iloc[:,1:14].values
        y_valid = valid["data"]["CLASS_NAME"].values
        #testing data 1 cross validation
        X_test = dataset_test["data"].iloc[:,1:14].values
        y_test = dataset_test["data"]["CLASS_NAME"].values
        #============================
        #Classification
        #============================
        #classifier= RandomForestClassifier(n_estimators=500)
        classifier= svm.SVC(C=4, kernel = 'rbf',gamma= 0.25)
        #training
        classifier.fit(X_train, y_train)
        #classifying validation and testing data
        result_valid = classifier.predict(X_valid)
        #result_test = classifier.predict(X_test)
        result_test = classifier.predict(X_test)
        #results validation
        as_valid =  accuracy_score(result_valid, y_valid)
        ks_valid =  cohen_kappa_score(result_valid, y_valid)
        print(f'Overal Accuracy validation : {as_valid}')
        print(f'Cohen_kappa validation : {ks_valid}')
        #results test 1
        as_test =  accuracy_score(result_test, y_test)
        ks_test =  cohen_kappa_score(result_test, y_test)
        print(f'Overal Accuracy test: {as_test}')
        print(f'Cohen_kappa test: {ks_test}')
        linetext = 'AS_Val: '+  str(as_valid) + ' KS_Val: ' + str(ks_valid) + ' AS_test: '+  str(as_test) + ' KS_test: ' + str(ks_test) + '\n'
        f.write(linetext)
        random = None
    #close the file with results
    f.close()
    print(f'done {i}')
