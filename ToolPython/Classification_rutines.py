#I want with this document to explore the accuraccies after validation of
#all the imagery over the Time
#240158
###   --folder_path  /home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST_Filter

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
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

#create object for classication
for i in list_folder_path:
    #preparing dataset
    dataset = al.import_data(os.path.join(i,"training_samples6_rf_w_queryB_85.shp"))  #training_samples3_rf_w_query #training_samples_sm.shp
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
    #creatinf file where I will store global accuraccies
    file_val = os.path.join(i,"validation_training_samples6_rf_w_queryB_85.shp.txt")  #validation_training_samples6_svm_w_queryB_85
    f= open(file_val,"w+")
    #validation random selection cross validation
    for j in range(0,20):
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
