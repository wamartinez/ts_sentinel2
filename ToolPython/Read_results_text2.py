###  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Autumn/IM_20170729/validation_modelIQR.txt

import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pathfile', help = 'path af the file txt')
    args =  parser.parse_args()
    print('start importation')

print("done")
f = open(args.pathfile, 'r')
#read lines
f1 =  f.readlines()
y = {}
x = []
w = 0
for k in f1:
    #appending lines
    k1 = k.split("PA:")[1]
    k2 = k1.split(" [")[1]
    k3 = k2.split("]")[0]
    k4 = k3.split(" ")
    x = []
    for i in range(0,15):
        x.append(k4[i])
    y[w] = x
    w= w + 1

df = pd.DataFrame(y)
df1 = df.T
print(df1)

file_name = '/home/user/Documents/TESISMASTER/csv/accuracies_7_29_2017.csv'
df1.to_csv(file_name, sep='\t')
