import argparse
#extract pixel values of the raster
#I think this function must add values. Insteof of creating a new shapefile is better only to update the shapefile.nayaway
#This task probabily will be done later, there i not too much time to rewrite everything
#After checking the previous proposal I think is better to add the raster by bands, tiff does not support file hevier than 4 gb
#WEELL, finally the decision is to add values by band and update chapefile, so I will leave this version without modificacion, so I will create a new version
# --input D:\TESISMASTER\VECTOR\Classification_2\training_samples_balance.shp
# --raster D:\TESISMASTER\IMAGES\COMPOSITIONS\composition_NDVI.tiff
# --output D:\TESISMASTER\VECTOR\Classification_2\Analysis_Outliers\training_samples_balance_ndvi.shp

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',help='Path of the input shapefile')
    parser.add_argument('--raster',help = 'Path of the raster folder')
    parser.add_argument('--output',help = 'Path of the output shapefile')
    args = parser.parse_args()
    print("Processing: " + args.input)
    print("Processing: " + args.raster)

##Importing shapefile
from osgeo import ogr, gdal, osr
import os
import numpy as np

driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.Open(args.input)
#Get layer
layer =  datasource.GetLayer()
proj_input = layer.GetSpatialRef()
fc = layer.GetFeatureCount()
layer_defn = layer.GetLayerDefn()
count_field = layer_defn.GetFieldCount()

#Getting name of the fiels of the Shapefile

schema = []
for k in range(0,count_field):
    f_field = layer_defn.GetFieldDefn(k)
    schema.append(f_field.name)

#importing rows
x = []
y = []
f2 = []
l=0
for fea in layer:
    pt = fea.geometry()
    x.append(pt.GetX())
    y.append(pt.GetY())
    f1 = []
    for i in range(0, count_field):
        field = fea.GetField(i)
        f1.append(field)
    #second part
    f2.append(f1)

#====================
#Importing raster
#====================

raster_dataset = gdal.Open(args.raster)
gt = raster_dataset.GetGeoTransform()
proj = raster_dataset.GetProjectionRef()

bands_data = []
n_bands = raster_dataset.RasterCount
for i in range(1,n_bands + 1):
    band = raster_dataset.GetRasterBand(i)
    bands_data.append(band.ReadAsArray())

bands_data = np.dstack(bands_data)

#===============================
#Intersecting raster and points
#===============================

#inverse of the geotransformation
inv_gt = gdal.InvGeoTransform(gt)
xt_p = []
yt_p = []

print(inv_gt)

for k in range(0,fc):
    xt , yt = gdal.ApplyGeoTransform(inv_gt[1], x[k], y[k])
    xt_p.append(xt)
    yt_p.append(yt)
#=========warning======================
##plase change inv_gt[1] by only inv_gt
#======================================
#intersecting

value = []
for i in range(0,fc):
    value.append(bands_data[int(yt_p[i]),int(xt_p[i]),:])

#=========================
#Creating output file
#=========================

#Set again driver
driver2 = ogr.GetDriverByName('ESRI Shapefile')

if os.path.exists(args.output):
    print('Deleting')
    driver2.DeleteDataSource(args.output)
#Create the spatial reference

#Create the output data source
points_datasource = driver2.CreateDataSource(args.output)
points_layer = points_datasource.CreateLayer('output', proj_input,geom_type = ogr.wkbPoint)

#Importin previous count_fields
label_layer = []
for i in range(0, count_field):
    old_field = ogr.FieldDefn(schema[i],ogr.OFTString)
    points_layer.CreateField(old_field)

#Create new fields
label_f_list = []
for i in range(0,n_bands):
    label_f = 'B_' + str(i+1)
    new_field = ogr.FieldDefn(label_f,ogr.OFTReal)
    label_f_list.append(label_f)
    points_layer.CreateField(new_field)

#Loading values to shapefile
j=0

for j in range(0, fc):
    #create points
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(x[j], y[j])
    #Create new feature
    feat = ogr.Feature(points_layer.GetLayerDefn())
    feat.SetGeometry(point)
    #add fields
    for w in range(0,count_field):
        feat.SetField(schema[w],f2[j][w])
    for d in range(0, n_bands):
        feat.SetField(label_f_list[d],np.float32(value[j][d]).item())
    points_layer.CreateFeature(feat)
    feat = None

datasource.Destroy()
points_datasource.Destroy()
print('Done')
