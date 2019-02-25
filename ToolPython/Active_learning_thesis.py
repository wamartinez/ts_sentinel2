#====================================
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import fetch_mldata
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler  #StandardScaler
from sklearn.svm import SVC
import os
from sklearn import svm
import Active_learning as al
import numpy as np
from osgeo import gdal, ogr
from sklearn.metrics import accuracy_score
import pandas as pd

#====================================
# "training_samples3.shp"

folder_path = r'D:\TESISMASTER\VECTOR\Training_data_ImageryST\TEMP'
list_folder_path = [os.path.join(folder_path , i) for i in os.listdir(folder_path)]
list_folder_path.sort()
for i in list_folder_path:
    print(f'processing file {i}')
    dataset_train = al.import_data(os.path.join(i,"training_samples11_Noise210.shp"))
    rows, cols = dataset_train["data"].shape
    #calling test 1 and test2
    dataset_test1 = al.import_data(os.path.join(i,"test_samples11.shp"))
    dataset_test2 = al.import_data(os.path.join(i,"BD_REF_HUGO2_11.shp"))
    #===============
    #Batch learning
    #===============
    #Sequence for Iteration
    a = np.arange(0,30,1).tolist()
    #clf = al.rf_model()
    clf = al.SvmModel()
    file_val = os.path.join(i,"validation_active_learning.txt")
    f= open(file_val,"w+")
    for k in a:
        print(f'Iteration k: {k}')
        entropies = al.entropy_rutines(dataset_train, clf, pivot = 'CLASS_NAME')
        #selection entropies
        entropies_order = np.argsort(entropies)
        #selecting most informative samples according with the threshold k
        ind_entropies_order = entropies_order[100:]
        query_ind = ind_entropies_order.tolist()
        print(len(query_ind))
        #queryng dataset_train
        dataset_train = {
            "coordinates":dataset_train["coordinates"].loc[query_ind].reset_index(drop =True),
            "data":dataset_train["data"].loc[query_ind].reset_index(drop =True),
            "proj":dataset_train["proj"]
        }
        X_train = dataset_train["data"].iloc[:,1:].values
        y_train = dataset_train["data"]["CLASS_NAME"].values
        #Calling test dataset 1 and 2
        X_test1 = dataset_test1["data"].iloc[:,1:].values
        y_test1 = dataset_test1["data"]["CLASS_NAME"].values
        #classifier= RandomForestClassifier(n_estimators=500)
        classifier= svm.SVC(C=4, kernel = 'rbf',gamma= 0.25)
        #training
        classifier.fit(X_train, y_train)
        #classifying validation and testing data
        result_test1 = classifier.predict(X_test1)
        #results validation
        oa =  accuracy_score(result_test1, y_test1)
        print(f'Overal Accuracy validation : {oa}')
        entropies = None
        #writing Document
        #accuracy_score producer per class in validation
        print(np.unique(y_test1))
        cm = confusion_matrix(result_test1, y_test1,labels = np.unique(y_test1))
        np.set_printoptions(precision=2)
        pr = np.diag(cm)
        sum_true = np.apply_along_axis(sum,1,cm)
        pr_label_true = np.divide(pr, sum_true)
        print('Accuracy producer: ', pr_label_true)
        #saving file
        linetext = ' AS_Val: ' + str(oa)  + ' PAtrue: ' + str(pr_label_true) + '\n'
        f.write(linetext)
        random = None
    #close the file with results
    f.close()
    print(f'done {i}')
