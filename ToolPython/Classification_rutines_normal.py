#I want with this document to explore the accuraccies after validation of
#all the imagery over the Time
#240158
###   --folder_path D:\TESISMASTER\VECTOR\Training_data_ImageryST\TEMP

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

list_folder_path = [i for i in os.listdir(args.folder_path)]
list_folder_path.sort()
print(list_folder_path)
number_iterations = 40
df_total = None
#create object for classication
for i in list_folder_path:
    #preparing dataset for mdelling
    dataset = al.import_data(os.path.join(args.folder_path,i,"training_samples11.shp"))
    #pereparing dataset for testing
    dataset_testing1 = al.import_data(os.path.join(args.folder_path,i,"test_samples11.shp"))
    dataset_testing2 = al.import_data(os.path.join(args.folder_path,i,"test_samples11.shp"))
    #creating file where I will store results of predicion of traning and testing of validation and testing
    list_iter = {}
    #validation random selection cross validation
    for j in range(0,number_iterations):
        #spliting data in training and validation
        random = al.random_selection(dataset,prob = 0.7, pivot= "CLASS_NAME")
        (train,valid) = random.stratified_random_selection()
        X_train = train["data"].iloc[:,1:14].values
        y_train = train["data"]["CLASS_NAME"].values
        X_valid = valid["data"].iloc[:,1:14].values
        y_valid = valid["data"]["CLASS_NAME"].values
        #testing data 1 external
        X_test1 = dataset_testing1["data"].iloc[:,1:14].values
        y_test1 = dataset_testing1["data"]["CLASS_NAME"].values
        #testing data 2 external
        X_test2 = dataset_testing2["data"].iloc[:,1:14].values
        y_test2 = dataset_testing2["data"]["CLASS_NAME"].values
        #============================
        #Classification
        #============================
        classifier= RandomForestClassifier(n_estimators=500)
        #classifier= svm.SVC(C=4, kernel = 'rbf',gamma= 0.25)
        #classifier = KNeighborsClassifier(n_neighbors = 10)
        #training
        classifier.fit(X_train, y_train)
        #classifying validation and testing data
        result_valid = classifier.predict(X_valid)
        result_test1 = classifier.predict(X_test1)
        result_test2 = classifier.predict(X_test2)
        #results validation
        as_valid =  accuracy_score(result_valid, y_valid)
        ks_valid =  cohen_kappa_score(result_valid, y_valid)
        print(f'Overal Accuracy validation : {as_valid}')
        print(f'Cohen_kappa validation : {ks_valid}')
        #results test 1
        as_test1 =  accuracy_score(result_test1, y_test1)
        ks_test1 =  cohen_kappa_score(result_test1, y_test1)
        print(f'Overal Accuracy test 1: {as_test1}')
        print(f'Cohen_kappa test 1 : {ks_test1}')
        #results test 2
        as_test2 =  accuracy_score(result_test2, y_test2)
        ks_test2 =  cohen_kappa_score(result_test2, y_test2)
        print(f'Overal Accuracy test 2: {as_test2}')
        print(f'Cohen_kappa test 2 : {ks_test2}')
        #accuracy_score producer per class in validation
        print(np.unique(y_valid))
        print(np.unique(y_test1))
        print(np.unique(y_test2))
        cm = confusion_matrix(result_test1, y_test1,labels = np.unique(y_test1))
        np.set_printoptions(precision=2)
        sum_true = np.apply_along_axis(sum,1,cm)  #0 is producer, 1 is useeer
        pr = np.diag(cm)
        pr_label = np.divide(pr,sum_true)
        print('Overal Accuracy: ', pr_label)
        #saving file
        list_iter[j] = [as_valid,ks_valid,as_test1,ks_test1,as_test2,ks_test2] + pr_label.tolist()
        random = None
    #creating dataframe of the results
    df_iter = pd.DataFrame.from_dict(list_iter).T
    label_iter = pd.Series(np.repeat(i,number_iterations))
    #adding column label of iteration
    df_iter_label = pd.concat([label_iter , df_iter], axis = 1, ignore_index =True)
    #concatenating dataframes
    df_total = pd.concat([df_total , df_iter_label], axis = 0, ignore_index =True)
    print(f'done {i}')
#adding names to the columns of daataframe
df_total.columns = ["Iter","OA_VAL","KS_VAL","OA_Test1","KS_test1","OA_Test2","KS_test2"] + np.unique(y_valid).tolist()
df_total.to_csv(r"D:\TESISMASTER\csv\Results\Validation_rf11_.csv",sep='\t')
print(df_total)
