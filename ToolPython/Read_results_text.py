<<<<<<< HEAD
#This script summarize the results for testing and validation
# --pathfiles  /home/user/Documents/TESISMASTER/VECTOR/Training_data_ImageryST
=======
#This script read the files in txt format and import the text in list o numpy
# --pathfiles /home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST_filter_size3
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f


import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
<<<<<<< HEAD
import numpy as np
=======
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pathfiles', help = 'path with the folder where files suppose to be')
    args =  parser.parse_args()
    print('start importation')

name_folders = [i for i in os.listdir(args.pathfiles)]
name_folders.sort()
print(name_folders)
folders = [os.path.join(args.pathfiles,l) for l in os.listdir(args.pathfiles)]
folders.sort()
print(folders)

<<<<<<< HEAD
output_final = None

for l in folders:
    name_folder = l.split('/')[-1]
    file_txt = os.path.join(l , 'validation_training_samples8_svm.txt')
    print(file_txt)
    y_valid = {}  # dictionary for data frame with results of validation
    y_test = {}  # dictionary for data frame with results of testing
    w=0
    f = open(file_txt, 'r')
    #read lines
    f1 =  f.readlines()
    x_valid = []
    x_test = []
    for k in f1:
        #appending lines
        x_valid.append(float(k.split(" ")[1]))
        x_test.append(float(k.split(" ")[5]))
    #appending all the values
    y_valid[name_folders[w]]  = x_valid
    y_test[name_folders[w]]  = x_test
    w= w + 1
    #organizing data frames
    df_valid = pd.DataFrame(y_valid)
    df_test = pd.DataFrame(y_test)
    #organizing the data in order to render it in R using ggplot2
    #column with the time index
    label_time = pd.Series(np.repeat(name_folder,df_test.shape[0]))
    mergedf = pd.concat([label_time,df_valid, df_test], axis = 1, ignore_index =True)
    output_final =  pd.concat([output_final,mergedf], axis = 0, ignore_index =True)
    #end loop
output_final.columns = ["Time","valid","test"]
print(output_final)
file_name = '/home/user/Documents/TESISMASTER/csv/Results/Validation_models/valid.csv'
output_final.to_csv(file_name, sep='\t')
print("done")
=======
y = {}
w=0
for j in folders:
    file = os.path.join(j,'validation_training_samples6_svm_w_queryA_70.txt')
    f = open(file, 'r')
    #read lines
    f1 =  f.readlines()
    x = []
    for k in f1:
        #appending lines
        #for overall accuracies
        x.append(float(k.split(" ")[1]))
        #for individual accuracies
        #k1 = k.split("PA:")[1]
        #k2 = k1.split(" [")[1]
        #k3 = k2.split("]")[0]
        #k4= k3.split(" ")[14]
        #x.append(float(k4))
    #appending all the values
    y[name_folders[w]]  = x
    w= w + 1

df = pd.DataFrame(y)

print(df)
file_name = '/home/user/Documents/TESISMASTER/csv/Results/Validation_models/validation.csv'
df.to_csv(file_name, sep='\t')
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
