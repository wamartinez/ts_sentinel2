<<<<<<< HEAD
#this schrip gives score of the trainng data that is likely outlierself.
#Based on the NDVI, I separete the values that are beyond the interquantile range and score then according
#with the number of times that they apper during the year

#Moreover, I think is better to have a shapefile that get the NDVI values form different rasters
#and automatically must gice you a score by each time

#--input_shapefile D:\TESISMASTER\VECTOR\Classification_2\Analysis_Outliers\training_samples_balance_ndvi.shp
#--output D:\TESISMASTER\VECTOR\Classification_2\Analysis_Outliers\training_samples_outliers_balance_2d.shp
#--type_limit 2d

import argparse
import numpy as np
import os
from osgeo import gdal, osr ,ogr
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_shapefile', help = 'path of the shapefile with training data and NDVI')
    parser.add_argument('--output', help = 'Path of the output shapefile')
    parser.add_argument('--type_limit', help = 'Threshold type')
    args = parser.parse_args()
    print('processing shapefiles in the folder:' + args.input_shapefile)


#===============================
#Opening shapefiles
#===============================
list_ndvi_byband = []
list_score_byband = []
driver = ogr.GetDriverByName('ESRI Shapefile')
data_source = driver.Open(args.input_shapefile)
layer = data_source.GetLayer()
fc = layer.GetFeatureCount()
proj = layer.GetSpatialRef()
layer_defn = layer.GetLayerDefn()
count_field = layer_defn.GetFieldCount()

#schema: name the of the columns
schema = []
for k in range(0,count_field):
    f_field = layer_defn.GetFieldDefn(k)
    schema.append(f_field.name)

#importing deatures in a list
x = []
y = []
f2 = []
#Importing features
for feat in layer:
    pt = feat.geometry()
    x.append(pt.GetX())
    y.append(pt.GetY())
    f1 = []
    for i in range(0, count_field):
        field = feat.GetField(i)
        f1.append(field)
    #second part
    f2.append(f1)

#converting list to dataframe
df=pd.DataFrame(f2,columns=schema)

#Calculating outliers

index = []
index2 = []
outlier_list = []

for k in range(1,(len(schema))):
    list_classes = np.unique(df.iloc[:,0])
    outlier_class = []
    for i in list_classes:
        index = np.where(df.iloc[:,0] == i)[0]
        if args.type_limit == 'ri':
            perc_25 = np.percentile(df.iloc[index,k],25)
            perc_75 = np.percentile(df.iloc[index,k],75)
            IQR = perc_75 - perc_25
            lim_rigth = perc_75 + IQR*1.5
            lim_left = perc_25 - IQR*1.5
        elif args.type_limit == '2d':
            mean = np.mean(df.iloc[index,k])
            sd = np.std(df.iloc[index,k])
            lim_rigth = mean + 2*sd
            lim_left = mean - 2*sd
        index2 = np.where((df.iloc[index,k] < lim_left) | (df.iloc[index,k] > lim_rigth))[0]
        outlier_class = outlier_class + index[index2].tolist()
        vector_score = np.zeros(fc)
        #score of 1 for those that are beyond the interquantile range
        vector_score[outlier_class] = 1
    #these are the outliers by column
    outlier_list.append(vector_score)

print('Outliers identified')
print(outlier_list)
print(schema)
print(len(outlier_list))

#================================================
#Creating shapefile with the fields with scores
#================================================
driver2 = ogr.GetDriverByName('ESRI Shapefile')
if os.path.exists(args.output):
    print('Deleting')
    driver2.DeleteDataSource(args.output)

point_datasource =  driver2.CreateDataSource(args.output)
points_layer = point_datasource.CreateLayer('output',proj, geom_type =  ogr.wkbPoint)
#create field class
field_oldclass = ogr.FieldDefn(schema[0], ogr.OFTString)
points_layer.CreateField(field_oldclass)

#Creating fields
Name_fields_score = []
for l in range(0, len(outlier_list)):
    #field with the classes
    Namef_score = 'ScoreIM' + str(l+1)
    field_ndvi = ogr.FieldDefn(schema[l+1], ogr.OFTReal)
    points_layer.CreateField(field_ndvi)
    field_score = ogr.FieldDefn(Namef_score, ogr.OFTReal)
    points_layer.CreateField(field_score)
    Name_fields_score.append(Namef_score)

#Loading values to shapefile
for j in range(0,fc):
    #Create points
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(x[j], y[j])
    #Create features
    feat = ogr.Feature(points_layer.GetLayerDefn())
    feat.SetGeometry(point)
    #Add fields of the input shapefile
    for k in range(0,len(schema)):
        feat.SetField(schema[k],df.iloc[j,k])
    #Add fields scores
    for w in range(0,len(Name_fields_score)):
        feat.SetField(Name_fields_score[w],outlier_list[w][j])
    points_layer.CreateFeature(feat)
    feat = None

point_datasource.Destroy()
print('It is Done')
=======
#this schrip gives score of the trainng data that is likely outlierself.
#Based on the NDVI, I separete the values that are beyond the interquantile range and score then according
#with the number of times that they apper during the year

#Moreover, I think is better to have a shapefile that get the NDVI values form different rasters
#and automatically must gice you a score by each time

#--input_shapefile D:\TESISMASTER\VECTOR\Classification_2\Analysis_Outliers\training_samples_balance_ndvi.shp
#--output D:\TESISMASTER\VECTOR\Classification_2\Analysis_Outliers\training_samples_outliers_balance_2d.shp
#--type_limit 2d

import argparse
import numpy as np
import os
from osgeo import gdal, osr ,ogr
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_shapefile', help = 'path of the shapefile with training data and NDVI')
    parser.add_argument('--output', help = 'Path of the output shapefile')
    parser.add_argument('--type_limit', help = 'Threshold type')
    args = parser.parse_args()
    print('processing shapefiles in the folder:' + args.input_shapefile)


#===============================
#Opening shapefiles
#===============================
list_ndvi_byband = []
list_score_byband = []
driver = ogr.GetDriverByName('ESRI Shapefile')
data_source = driver.Open(args.input_shapefile)
layer = data_source.GetLayer()
fc = layer.GetFeatureCount()
proj = layer.GetSpatialRef()
layer_defn = layer.GetLayerDefn()
count_field = layer_defn.GetFieldCount()

#schema: name the of the columns
schema = []
for k in range(0,count_field):
    f_field = layer_defn.GetFieldDefn(k)
    schema.append(f_field.name)

#importing deatures in a list
x = []
y = []
f2 = []
#Importing features
for feat in layer:
    pt = feat.geometry()
    x.append(pt.GetX())
    y.append(pt.GetY())
    f1 = []
    for i in range(0, count_field):
        field = feat.GetField(i)
        f1.append(field)
    #second part
    f2.append(f1)

#converting list to dataframe
df=pd.DataFrame(f2,columns=schema)

#Calculating outliers

index = []
index2 = []
outlier_list = []

for k in range(1,(len(schema))):
    list_classes = np.unique(df.iloc[:,0])
    outlier_class = []
    for i in list_classes:
        index = np.where(df.iloc[:,0] == i)[0]
        if args.type_limit == 'ri':
            perc_25 = np.percentile(df.iloc[index,k],25)
            perc_75 = np.percentile(df.iloc[index,k],75)
            IQR = perc_75 - perc_25
            lim_rigth = perc_75 + IQR*1.5
            lim_left = perc_25 - IQR*1.5
        elif args.type_limit == '2d':
            mean = np.mean(df.iloc[index,k])
            sd = np.std(df.iloc[index,k])
            lim_rigth = mean + 2*sd
            lim_left = mean - 2*sd
        index2 = np.where((df.iloc[index,k] < lim_left) | (df.iloc[index,k] > lim_rigth))[0]
        outlier_class = outlier_class + index[index2].tolist()
        vector_score = np.zeros(fc)
        #score of 1 for those that are beyond the interquantile range
        vector_score[outlier_class] = 1
    #these are the outliers by column
    outlier_list.append(vector_score)

print('Outliers identified')
print(outlier_list)
print(schema)
print(len(outlier_list))

#================================================
#Creating shapefile with the fields with scores
#================================================
driver2 = ogr.GetDriverByName('ESRI Shapefile')
if os.path.exists(args.output):
    print('Deleting')
    driver2.DeleteDataSource(args.output)

point_datasource =  driver2.CreateDataSource(args.output)
points_layer = point_datasource.CreateLayer('output',proj, geom_type =  ogr.wkbPoint)
#create field class
field_oldclass = ogr.FieldDefn(schema[0], ogr.OFTString)
points_layer.CreateField(field_oldclass)

#Creating fields
Name_fields_score = []
for l in range(0, len(outlier_list)):
    #field with the classes
    Namef_score = 'ScoreIM' + str(l+1)
    field_ndvi = ogr.FieldDefn(schema[l+1], ogr.OFTReal)
    points_layer.CreateField(field_ndvi)
    field_score = ogr.FieldDefn(Namef_score, ogr.OFTReal)
    points_layer.CreateField(field_score)
    Name_fields_score.append(Namef_score)

#Loading values to shapefile
for j in range(0,fc):
    #Create points
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(x[j], y[j])
    #Create features
    feat = ogr.Feature(points_layer.GetLayerDefn())
    feat.SetGeometry(point)
    #Add fields of the input shapefile
    for k in range(0,len(schema)):
        feat.SetField(schema[k],df.iloc[j,k])
    #Add fields scores
    for w in range(0,len(Name_fields_score)):
        feat.SetField(Name_fields_score[w],outlier_list[w][j])
    points_layer.CreateFeature(feat)
    feat = None

point_datasource.Destroy()
print('It is Done')
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
