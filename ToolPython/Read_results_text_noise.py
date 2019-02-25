#This script summarize the results for testing and validation
# --pathfiles /home/user/Documents/TESISMASTER/VECTOR/Noise/Noise_6_classes/Results/SVM


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


list_folder_path = [os.path.join(args.pathfiles, i) for i in os.listdir(args.pathfiles) if i.endswith(".txt")]
list_folder_path.sort()
print(list_folder_path)


output = None
for l in list_folder_path:
    level_noise = l.split('.')[0][-7:]
    y_test = {}  # dictionary for data frame with results of testing
    f = open(l, 'r')
    #read lines
    f1 =  f.readlines()
    x_test = []
    for k in f1:
        #appending lines
        x_test.append(float(k.split(" ")[5]))
    #appending all the values
    y_test[level_noise]  = x_test
    #organizing data frames
    df_test = pd.DataFrame(y_test)
    #organizing the data in order to render it in R using ggplot2
    label_noise = pd.Series(np.repeat(level_noise, df_test.shape[0]))
    label_noise_test = pd.concat([label_noise, df_test], axis = 1, ignore_index =True)
    label_noise_test.columns = ["Noise","Accuracy"]
    output = pd.concat([output,label_noise_test], axis = 0,ignore_index =True)
    #end loop

print(output.head())
file_name = '/home/user/Documents/TESISMASTER/csv/Results/Validation_models/valid2.csv'
output.to_csv(file_name, sep='\t')
print("done")
