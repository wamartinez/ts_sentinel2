#This script attempt to document the process of emooving the outliers of the traning raster_dataset
# --input D:\TESISMASTER\VECTOR\Classification_2\Analysis_Outliers\training_samples_outliers_balance.shp
# --tr 2
# --output D:\TESISMASTER\VECTOR\Classification_2\split_training_model2

import argparse
from osgeo import ogr
import os
import numpy as np

if __name__ == '__main__':
    parser =  argparse.ArgumentParser()
    parser.add_argument('--input', help = 'shapefile with scores')
    parser.add_argument('--tr', help = 'Threshold for the scores')
    parser.add_argument('--output', help = 'Folder where is stored the training data')
    args =  parser.parse_args()
    print('processing' + args.input)


driver =  ogr.GetDriverByName('ESRI Shapefile')
datasource =  driver.Open(args.input)
layer = datasource.GetLayer()
proj = layer.GetSpatialRef()


x = []
y = []
class_name = []

for fea in layer:
    score = fea.GetField('Score')
    if score < int(args.tr):
        pt = fea.geometry()
        x.append(pt.GetX())
        y.append(pt.GetY())
        class_name.append(fea.GetField('CLASS_NAME'))

#=========================================
#Creating shapefiles with the new features
#=========================================

name_classes = np.unique(class_name)
#converting list in arrays
x = np.array(x)
y = np.array(y)
class_name = np.array(class_name)

#Set again driver
i = 1
for k in name_classes:
    output = os.path.join(args.output, str(i)  + ".shp")
    driver2 = ogr.GetDriverByName('ESRI Shapefile')
    points_datasource = driver2.CreateDataSource(output)
    #creating pointdata source
    points_layer = points_datasource.CreateLayer(str(i), proj , geom_type = ogr.wkbPoint)
    #creating fields
    field_class = ogr.FieldDefn('CLASS_NAME' ,ogr.OFTString)
    points_layer.CreateField(field_class)
    field_code = ogr.FieldDefn('CODE' ,ogr.OFTReal)
    points_layer.CreateField(field_code)
    #Adding features
    index = np.where(class_name == k)[0]
    for j in range(0,len(index)):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(x[index[j]], y[index[j]])
        #Create new feature
        feat = ogr.Feature(points_layer.GetLayerDefn())
        feat.SetGeometry(point)
        #add fields
        feat.SetField('CLASS_NAME',class_name[index[j]])
        feat.SetField('CODE',i)
        points_layer.CreateFeature(feat)
        feat = None
    i = i + 1
    points_datasource.Destroy()
    driver2 = None
    feat = None



datasource.Destroy()
print('Done')
