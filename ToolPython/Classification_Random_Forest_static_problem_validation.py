#    /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Winter
#======================================================================
#This script attempts to set baseline of the standart static approach
#======================================================================
# --train_path /home/user/Documents/TESISMASTER/VECTOR/Analysis_outliers/Model_IQR
# --raster_path /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Composites_pca
#======================================================================
#Parsing information
#======================================================================
import argparse
from osgeo import gdal, ogr
import os
import numpy as np
import lulc
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
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

file_DEM = "/home/user/Documents/TESISMASTER/ZDEM/ZDEM_10m.tiff"
file_Slope = "/home/user/Documents/TESISMASTER/ZDEM/ZSLOPE_10m.tiff"

list_folder = [os.path.join(args.raster_path,i) for i in os.listdir(args.raster_path)]
list_folder.sort()

for k in list_folder:
    print('processing: ', k)
    #Creating fie with results of the validation
    file = os.path.join(k,"validation_modelNone.txt")
    f= open(file,"w+")
    #importing path of the rasters
    list_raster = [os.path.join(k,i) for i in os.listdir(k) if i.endswith('.tiff') or i.endswith('.jp2')]
    list_raster.append(file_DEM)
    list_raster.append(file_Slope)
    list_raster.sort()
    #names of the raster_dataset
    list_label_raster = [i.split('_')[-2] for i in os.listdir(k) if i.endswith('.tiff') or i.endswith('.jp2')]
    list_label_raster.append('Z_DEM')
    list_label_raster.append('Z_Slope')
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

    #Importing shapefiles
    print('Calling shapefiles')
    shapefiles = [os.path.join(args.train_path,i) for i in os.listdir(args.train_path) if i.endswith('.shp')]
    shapefiles.sort()
    print(shapefiles)
    labels_classes = [i.split('.')[0] for i in os.listdir(args.train_path) if i.endswith('.shp')]
    labels_classes.sort()
    print(labels_classes)
    #Rasterizing the training data
    labeled_pixels= lulc.vectors_to_raster(shapefiles, rows, cols, gt , proj)


    #selecting training data,
    is_train= np.nonzero(labeled_pixels)
    training_labels = labeled_pixels[is_train]
    training_samples = bands_data[is_train]
    print(training_samples.shape)

    #=======================
    # Modelling
    #=======================
    #=======================
    # stratiffing by class
    #=======================
    print('Start validation')

    for l in range(0,20):
        accuracy = []
        tr, tes = lulc.stratified_sampling(training_labels,prob = (0.7,0.3))
        #train
        train_samples = training_samples[tr,]
        train_labels = training_labels[tr,]
        #test
        test_samples = training_samples[tes,]
        test_labels = training_labels[tes,]
        #========================
        #Decision tree Classifier
        #========================
        classifier= RandomForestClassifier(n_estimators=100,min_samples_split = 4)
        classifier.fit(train_samples, train_labels)
        result = classifier.predict(test_samples)
        print(np.unique(test_labels))
        #probabilities_result = classifier.predict_proba(test_samples)
        #print(probabilities_result)
        #========================
        #Hitmap confusion matrix
        #========================
        cm = confusion_matrix(test_labels,result,labels = np.unique(test_labels))
        np.set_printoptions(precision=2)
        # Plot normalized confusion matrix
        oa = accuracy_score(test_labels,result)
        print('Overal Accuracy: ', oa)
        accuracy.append(oa)
        sum_true = np.apply_along_axis(sum,1,cm)
        pr = np.diag(cm)
        pr_label = np.divide(pr,sum_true)
        print('Overal Accuracy: ', pr_label)
        accuracy.append(pr_label)
        #saving file
        linetext = 'OA: '+  str(accuracy[0]) + ' PA: ' + str(accuracy[1]) + '\n'
        f.write(linetext)
        #====================
        #Feature importances
        #====================
        print(np.unique(test_labels))
        print(classifier.feature_importances_)
        print('Loop validation ', l)
    #close the file with results
    f.close()
    print('done', k)
