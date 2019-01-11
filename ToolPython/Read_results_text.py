#This script read the files in txt format and import the text in list o numpy
# --pathfiles /home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST_filter_size3


import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt

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
