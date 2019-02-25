<<<<<<< HEAD
#    /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Winter
#======================================================================
#This script attempts to set baseline of the standart static approach
#======================================================================
# --train_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/VECTOR/STATIC/IM_20170729/training_samples7_rf_w_queryA_80_out.shp
# --raster_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/STATIC/IM_20170729
#======================================================================
#Parsing information
#======================================================================
import argparse
from osgeo import gdal, ogr
import os
import numpy as np
import lulc
import pandas as pd
import Active_learning as al
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path',help='training data path')
    parser.add_argument('--raster_path',help='raster data path')
    args = parser.parse_args()
    print('start processing')

#=============================
#Importing imagery from folder
#=============================
output_file = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/PREDICTION/COMPOSITES/IM_20170729_80AF0.tif"
file_DEM = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/ZDEM/IM_2017_ZDEM_10m.tiff"
file_Slope = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/ZDEM/IM_2017_ZSLOPE_10m.tiff"
#importing path of the raster files

#importing path of the rasters
list_raster = [os.path.join(args.raster_path,i) for i in os.listdir(args.raster_path) if i.endswith('.tiff') or i.endswith('.jp2')]
list_raster.append(file_DEM)
list_raster.append(file_Slope)
list_raster.sort()
print(list_raster)
#names of the raster_dataset
list_label_raster = [i.split('_')[-2] for i in os.listdir(args.raster_path) if i.endswith('.tiff') or i.endswith('.jp2')]
list_label_raster.append('ZDEM')
list_label_raster.append('ZSLOPE')
list_label_raster.sort()
print('Bands in process')
print(list_label_raster)

bands_data = []
for i in list_raster:
    raster_dataset = gdal.Open(i,gdal.GA_ReadOnly)
    #geotransformation
    gt = raster_dataset.GetGeoTransform()
    proj = raster_dataset.GetProjectionRef()
    #Importing bands as a set of arrays
    n_bads = raster_dataset.RasterCount
    band =  raster_dataset.GetRasterBand(1)
    bands_data.append(band.ReadAsArray())
    print('Band: ', i, ' is imported')
    raster_dataset = None
#stacking layers
bands_data = np.dstack(bands_data)
rows, cols, n_bands= bands_data.shape

#============================================
#Importing shapefile for training
#============================================
dataset = al.import_data(args.train_path)
#slicing variables of interest
data = dataset["data"].iloc[:,1:14]
col_names = data.dtypes.index.tolist()
data_standard = data #StandardScaler().fit_transform(data)
data_standard_df = pd.DataFrame(data_standard,columns = col_names)
labels = dataset["data"].iloc[:,0]
dataset_standard_df = pd.concat([labels,data_standard_df], axis = 1)
dataset_standard = {
    "coordinates":dataset["coordinates"],
    "data":dataset_standard_df,
    "proj":dataset["proj"]
}
#random selectin of 70% of the information
random = al.random_selection(dataset_standard,prob = 0.7, pivot= "CLASS_NAME")
(train,test) = random.stratified_random_selection()
X_train = train["data"].iloc[:,1:14].values
y_train = train["data"]["CLASS_NAME"].values
#print(X_train)
#print(y_train)
#classifier
print("trining classifier")
#classifier= RandomForestClassifier(n_estimators=500)
classifier= svm.SVC(C=4, kernel = 'rbf',gamma= 0.25)
classifier.fit(X_train,y_train)
#classificationf of the image
random = None
X_train = None
y_train = None
train = None
test = None

print("classifying pixels")
n_samples = rows * cols
flat_pixels = bands_data.reshape((n_samples,n_bands))
result = classifier.predict(flat_pixels)
result1 = np.array([int(i) for i in result])
#print(type(result1))
classification = result1.reshape((rows,cols))
lulc.write_geotiff(output_file,classification, gt, proj)
print("done")
=======
#    /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Winter
#======================================================================
#This script attempts to set baseline of the standart static approach
#======================================================================
# --train_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/VECTOR/STATIC/IM_20170405/training_samples6_rf_w_queryA_70_out.shp
# --raster_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/STATIC/IM_20170405
#======================================================================
#Parsing information
#======================================================================
import argparse
from osgeo import gdal, ogr
import os
import numpy as np
import lulc
import pandas as pd
import Active_learning as al
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path',help='training data path')
    parser.add_argument('--raster_path',help='raster data path')
    args = parser.parse_args()
    print('start processing')

#=============================
#Importing imagery from folder
#=============================
output_file = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/PREDICTION/STATIC/IM_20171216_70AF3.tif"
file_DEM = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/ZDEM/IM_2017_ZDEM_10m.tiff"
file_Slope = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/ZDEM/IM_2017_ZSLOPE_10m.tiff"
#importing path of the raster files

#importing path of the rasters
list_raster = [os.path.join(args.raster_path,i) for i in os.listdir(args.raster_path) if i.endswith('.tiff') or i.endswith('.jp2')]
list_raster.append(file_DEM)
list_raster.append(file_Slope)
list_raster.sort()
print(list_raster)
#names of the raster_dataset
list_label_raster = [i.split('_')[-2] for i in os.listdir(args.raster_path) if i.endswith('.tiff') or i.endswith('.jp2')]
list_label_raster.append('ZDEM')
list_label_raster.append('ZSLOPE')
list_label_raster.sort()
print('Bands in process')
print(list_label_raster)

bands_data = []
for i in list_raster:
    raster_dataset = gdal.Open(i,gdal.GA_ReadOnly)
    #geotransformation
    gt = raster_dataset.GetGeoTransform()
    proj = raster_dataset.GetProjectionRef()
    #Importing bands as a set of arrays
    n_bads = raster_dataset.RasterCount
    band =  raster_dataset.GetRasterBand(1)
    bands_data.append(band.ReadAsArray())
    print('Band: ', i, ' is imported')
    raster_dataset = None
#stacking layers
bands_data = np.dstack(bands_data)
rows, cols, n_bands= bands_data.shape

#============================================
#Importing shapefile for training
#============================================
dataset = al.import_data(args.train_path)
#slicing variables of interest
data = dataset["data"].iloc[:,1:14]
col_names = data.dtypes.index.tolist()
data_standard = data #StandardScaler().fit_transform(data)
data_standard_df = pd.DataFrame(data_standard,columns = col_names)
labels = dataset["data"].iloc[:,0]
dataset_standard_df = pd.concat([labels,data_standard_df], axis = 1)
dataset_standard = {
    "coordinates":dataset["coordinates"],
    "data":dataset_standard_df,
    "proj":dataset["proj"]
}
#random selectin of 70% of the information
random = al.random_selection(dataset_standard,prob = 0.7, pivot= "CLASS_NAME")
(train,test) = random.stratified_random_selection()
X_train = train["data"].iloc[:,1:14].values
y_train = train["data"]["CLASS_NAME"].values
#print(X_train)
#print(y_train)
#classifier
print("trining classifier")
#classifier= RandomForestClassifier(n_estimators=500)
classifier= svm.SVC(C=4, kernel = 'rbf',gamma= 0.25)
classifier.fit(X_train,y_train)
#classificationf of the image
random = None
X_train = None
y_train = None
train = None
test = None

print("classifying pixels")
n_samples = rows * cols
flat_pixels = bands_data.reshape((n_samples,n_bands))
result = classifier.predict(flat_pixels)
result1 = np.array([int(i) for i in result])
#print(type(result1))
classification = result1.reshape((rows,cols))
lulc.write_geotiff(output_file,classification, gt, proj)
print("done")
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
