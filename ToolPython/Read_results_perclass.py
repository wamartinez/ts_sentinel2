#This script summarize the results for testing and validation
# --pathfiles D:\TESISMASTER\VECTOR\Training_data_ImageryST\TEMP\IM_20170729\temp\20170729

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

name_files = [i for i in os.listdir(args.pathfiles)]
name_files.sort()
print(name_files)
output_final = None

for l in name_files:
    number = l[-6:-4]
    file_txt = os.path.join(args.pathfiles , l)
    print(file_txt)
    #y_test = {}  # dictionary for data frame with results of testing
    f = open(file_txt, 'r')
    #read lines
    f1 =  f.readlines()
    accuracies = {}
    w = 0
    for k in f1:
        #appending lines
        k0 = k.split('[')[1]
        k1 = k0.split(']')[0]
        #print(k1.split(' '))
        accuracies[w] = k1.split(' ')[:6]
        w = w + 1
    #organizing data frames
    df_accuracies = pd.DataFrame.from_dict(accuracies).T
    #spliting data frame
    output_prefinal = None
    for j in range(1,df_accuracies.shape[1]+1):
        label_class = pd.Series(np.repeat(j,df_accuracies.shape[0]))
        cold_def = pd.concat([label_class , df_accuracies.iloc[:,j-1]], axis = 1, ignore_index =True)
        output_prefinal = pd.concat([output_prefinal,cold_def], axis = 0, ignore_index =True)
    #appending all the values
    label_infor = pd.Series(np.repeat(number, df_accuracies.shape[0]*df_accuracies.shape[1]))
    mergedf = pd.concat([label_infor,output_prefinal], axis = 1, ignore_index =True)
    output_final =  pd.concat([output_final,mergedf], axis = 0, ignore_index =True)
    #end loop

file_name = r'D:\TESISMASTER\csv\Results\Validation_models\valid.csv'
output_final.to_csv(file_name, sep='\t')
print("done")
