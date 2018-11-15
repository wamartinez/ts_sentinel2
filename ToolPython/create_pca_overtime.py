#the attempt of this script is to extract the bands per time and calculate
#the principal components, so that I can update one shapefile with only the
#first principalper time
#I will call the files accorsing with the season
# --data_folder /home/user/Documents/TESISMASTER/VECTOR/Training_data_espectral_time/Summer
# --output  /home/user/Documents/TESISMASTER/VECTOR/Training_data_espectral_time/Result/training_samples.shp

import argparse
import lulc
import pandas as pd
from osgeo import ogr
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_folder',help='Path of shapefiles with information')
    parser.add_argument('--output',help = 'Path of output shapefile')
    args = parser.parse_args()
    print("Processing shapefiles: " + args.output)


#IMporting path of the folder with the shapefiles
list_shapefiles = [os.path.join(args.data_folder,i,"training_samples.shp") for i in os.listdir(args.data_folder)]
list_shapefiles.sort()

#Importing names
list_names_folder = [i[3:] for i in os.listdir(args.data_folder)]
list_names_folder.sort()
print(list_names_folder)

pc1_time = []
for i in list_shapefiles:
    print(f'Processing file: {i}')
    pc_daf = lulc.pca_calculator(i)
    pc1_daf = pc_daf['pc2'].values
    #print(type(pc1_daf))
    #print(pc1_daf.head(4))
    #break
    pc1_time.append(pc1_daf.tolist())

print("Importing data pca to the shapefile")
#importing features and coordinates of the shapefile in a list
driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.Open(args.output,1)
layer2 = datasource.GetLayer()
for j in list_names_folder:
    print(f'Importing column {j}')
    new_field = ogr.FieldDefn(j, ogr.OFTReal)
    layer2.CreateField(new_field)
#importing features
i = 0
for feat in layer2:
    k = 0
    for z in list_names_folder:
        feat.SetField(z,pc1_time[k][i])
        k = k + 1
    i = i + 1
    layer2.SetFeature(feat)

datasource = None
print('Done')
