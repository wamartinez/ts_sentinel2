#I want with this document to explore the accuraccies after validation of
#all the imagery over the Time
#240158
<<<<<<< HEAD
###   --folder_path  D:\TESISMASTER\VECTOR\Training_data_ImageryST\TEMP\IM_20170729
=======
###   --folder_path  /home/user/Documents/TESISMASTER/VECTOR/Training_data_ImageryST
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
<<<<<<< HEAD
from sklearn.neighbors import KNeighborsClassifier
=======
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
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
<<<<<<< HEAD
    print(f'processing files in {args.folder_path}')

#Creatin levels of informativeness
levels = np.arange(0,0.6,0.01).tolist()
number_iterations = 20
df_total = None
for i in levels:
    #preparing dataset for mdelling
    dataset_w = al.import_data(os.path.join(args.folder_path,"training_samples11_Noise210_rf_w.shp"))
    #pereparing dataset for testing
    dataset_testing1 = al.import_data(os.path.join(args.folder_path,"test_samples11.shp"))
    dataset_testing2 = al.import_data(os.path.join(args.folder_path,"BD_REF_HUGO2_11.shp"))
    row, col = dataset_w["data"].shape
    #=============================================
    #imbalance removing  A
    #=============================================
    weights = dataset_w["data"].loc[:,"weights"]
    threshold = int(row*(float(i))) #45
    a = np.argsort(weights)
    #dataset with the most informative samples,450 represent 5%, it is my standart delta
    ind_a = a[threshold:]
    query_ind_a = ind_a.tolist()
    #queryng dataset_w, this data is going to be for validation
    dataset  = {}
    dataset = {
        "coordinates":dataset_w["coordinates"].loc[query_ind_a].reset_index(drop =True),
        "data":dataset_w["data"].loc[query_ind_a].reset_index(drop =True),
        "proj":dataset_w["proj"]
        }

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
        #classifier= RandomForestClassifier(n_estimators=500)
        classifier= svm.SVC(C=4, kernel = 'rbf',gamma= 0.25)
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
        np.set_printoptions(precision=2)
        cm_test1 = confusion_matrix(result_test1, y_test1,labels = np.unique(y_test1))
        cm_test2 = confusion_matrix(result_test2, y_test2,labels = np.unique(y_test2))
        sum_true_test1 = np.apply_along_axis(sum,1,cm_test1)
        sum_true_test2 = np.apply_along_axis(sum,1,cm_test2)
        pr_test1 = np.diag(cm_test1)
        pr_test2 = np.diag(cm_test2)
        pr_label_test1 = np.divide(pr_test1,sum_true_test1)
        pr_label_test2 = np.divide(pr_test2,sum_true_test2)
        print('Producer accuracies test1: ', pr_label_test1)
        print('Producer accuracies test2: ', pr_label_test2)
        random = None
        list_iter[j] = [as_valid,ks_valid,as_test1,ks_test1,as_test2,ks_test2] + pr_label_test1.tolist() + pr_label_test2.tolist()
    #creating dataframe of the results
    df_iter = pd.DataFrame.from_dict(list_iter).T
    label_iter = pd.Series(np.repeat(i,number_iterations))
    #adding column label of iteration
    df_iter_label = pd.concat([label_iter , df_iter], axis = 1, ignore_index =True)
    #concatenating dataframes
    df_total = pd.concat([df_total , df_iter_label], axis = 0, ignore_index =True)
    print(f'done {i}')
#adding names to the columns of daataframe
df_total.columns = ["Iter","OA_VAL","KS_VAL","OA_Test1","KS_test1","OA_Test2","KS_test2"] + np.unique(y_valid).tolist() + np.unique(y_valid).tolist()
df_total.to_csv(os.path.join(args.folder_path,"Active_learning_results_11_Noise30.csv"),sep='\t')
print(df_total)
=======
    print(args.folder_path)

list_folder_path = [os.path.join(args.folder_path, i) for i in os.listdir(args.folder_path)]
list_folder_path.sort()
print(list_folder_path)

#create object for classication
for i in list_folder_path:
    #preparing dataset
    dataset = al.import_data(os.path.join(i,"training_samples6_rf_w_queryA_85.shp"))  #training_samples3_rf_w_query #training_samples_sm.shp
    data = dataset["data"].iloc[:,1:14]
    #weights = dataset["data"].weights
    col_names = data.dtypes.index.tolist()
    data_standard = data # StandardScaler().fit_transform(data)
    data_standard_df = pd.DataFrame(data_standard,columns = col_names)
    labels = dataset["data"].iloc[:,0]
    dataset_standard_df = pd.concat([labels,data_standard_df], axis = 1)
    dataset_standard = {
        "coordinates":dataset["coordinates"],
        "data":dataset_standard_df,
        "proj":dataset["proj"]
    }
    #creating file where I will store global accuraccies
    file_val = os.path.join(i,"validation_training_samples6_rf_w_queryA_85.txt")  #validation_training_samples6_svm_w_queryB_85
    f= open(file_val,"w+")
    #validation random selection cross validation
    for j in range(0,50):
        accuracy = []
        kappa_score = []
        random = al.random_selection(dataset_standard,prob = 0.7, pivot= "CLASS_NAME")
        (train,test) = random.stratified_random_selection()
        X_train = train["data"].iloc[:,1:14].values
        y_train = train["data"]["CLASS_NAME"].values
        X_test = test["data"].iloc[:,1:14].values
        y_test = test["data"]["CLASS_NAME"].values
        #weights = train["data"]["weights"].values
        #random forest classification
        classifier= RandomForestClassifier(n_estimators=500)
        #classifier= svm.SVC(C=4, kernel = 'rbf',gamma= 0.25)
        classifier.fit(X_train,y_train)
        result = classifier.predict(X_test)
        #accuracy_score
        cm = confusion_matrix(y_test,result,labels = np.unique(y_test))
        np.set_printoptions(precision=2)
        #calculation overall accuracy user
        oa = accuracy_score(result, y_test)
        print('Overal Accuracy: ', oa)
        #kappa accuracy_score
        ak = cohen_kappa_score(result, y_test)
        print('Cohen_kappa: ', ak)
        accuracy.append(oa)
        kappa_score.append(ak)
        sum_true = np.apply_along_axis(sum,1,cm)
        pr = np.diag(cm)
        pr_label = np.divide(pr,sum_true)
        print('Overal Accuracy: ', pr_label)
        accuracy.append(pr_label)
        #saving file
        linetext = 'OA: '+  str(accuracy[0]) + ' SK: ' + str(kappa_score[0]) + ' PA: ' + str(accuracy[1]) + '\n'
        f.write(linetext)
        random = None
    #close the file with results
    f.close()
    print(f'done {i}')
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
