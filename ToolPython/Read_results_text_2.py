#This script summarize the results for testing and validation
# --pathfiles   /home/user/Documents/TESISMASTER/VECTOR/training_data_static_model_centralmeans


import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
#asumming I can find the same files in every folder

name_files = [j for j in os.listdir(os.path.join(args.pathfiles,folders[0])) if j.endswith(".txt")]
print(name_files)

output_final = None

for l in name_files:
    number_file = l.split(".")[0][-2:]
    y_valid = {}  # dictionary for data frame with results of validation
    y_test = {}  # dictionary for data frame with results of testing
    y_test2 = {}  # dictionary for data frame with results of testing 2
    w=0
    for j in folders:
        file = os.path.join(j,l)
        f = open(file, 'r')
        #read lines
        f1 =  f.readlines()
        x_valid = []
        x_test = []
        x_test2 = []
        for k in f1:
            #appending lines
            x_valid.append(float(k.split(" ")[1]))
            x_test.append(float(k.split(" ")[5]))
            x_test2.append(float(k.split(" ")[9]))
        #appending all the values
        y_valid[name_folders[w]]  = x_valid
        y_test[name_folders[w]]  = x_test
        y_test2[name_folders[w]]  = x_test2
        w= w + 1
    #organizing data frames
    df_valid = pd.DataFrame(y_valid)
    df_test = pd.DataFrame(y_test)
    df_test2 = pd.DataFrame(y_test2)
    #organizing the data in order to render it in R using ggplot2
    names_columns = list(df_valid.columns.values) #names of the colums, they suppose to have the same name
    print(names_columns)
    output = None
    for i in range(0,df_valid.shape[1]):
        col_valid = df_valid.iloc[:,i]
        col_test = df_test.iloc[:,i]
        col_test2 = df_test2.iloc[:,i]
        mergedf = pd.concat([col_valid, col_test, col_test2], axis = 0, ignore_index =True)
        #adding column with type of accuracy
        label_valid = pd.Series(np.repeat("Validation", df_valid.shape[0]))
        label_test = pd.Series(np.repeat("test", df_valid.shape[0]))
        label_test2 = pd.Series(np.repeat("test2", df_valid.shape[0]))
        label_valid_test = pd.concat([ label_valid, label_test, label_test2], axis = 0, ignore_index =True)
        #adding label of time
        label_time = pd.Series(np.repeat(names_columns[i], df_valid.shape[0]*3))
        mergedf_col_time = pd.concat([label_time,label_valid_test , mergedf], axis = 1,ignore_index =True)
        #adding label of number of informativeness
        label_time = pd.Series(np.repeat(number_file, df_valid.shape[0]*3))
        mergedf_col_label = pd.concat([label_time, mergedf_col_time ],  axis = 1,ignore_index =True)
        #finally, I Store this dataframe in a bag as n iteration
        output = pd.concat([output,mergedf_col_label], axis = 0,ignore_index =True)
        #end loop
    output.columns = ["Informativeness","Time","Type","Accuracy"]
    output_final = pd.concat([output,output_final], axis = 0,ignore_index =True)

print(output_final.head())
file_name = '/home/user/Documents/TESISMASTER/csv/Results/Validation_models/valid.csv'
output_final.to_csv(file_name, sep='\t')
print("done")
