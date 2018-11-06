import argparse
import lulc
#extract pixel values of the raster
#I think this function must add values. Insteof of creating a new shapefile is better only to update the shapefile.nayaway
#This task probabily will be done later, there i not too much time to rewrite everything
#After checking the previous proposal I think is better to add the raster by bands, tiff does not support file hevier than 4 gb
#WEELL, finally the decision is to add values by band and update chapefile, so I will leave this version without modificacion, so I will create a new version
# --input /home/user/Documents/TESISMASTER/VECTOR/Analysis_Outliers_Composites/training_samples.shp
# --raster /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/NDVI_Composites

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',help='Path of the input shapefile')
    parser.add_argument('--raster',help = 'Path of the raster path')
    args = parser.parse_args()
    print("Processing shapefile in: " + args.input)
    print("Processing images in: " + args.raster)

##Importing shapefile
from osgeo import ogr, gdal, osr
import os
import numpy as np

driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.Open(args.input)
#Get layer
layer =  datasource.GetLayer()
fc = layer.GetFeatureCount()
proj_input = layer.GetSpatialRef()
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

print("Ready coordinates")
#====================
#Importing raster
#====================

#=====================================

list_path_raster = [os.path.join(args.raster,w) for w in os.listdir(args.raster)]
list_path_raster.sort()
print("list of rasters")
print(list_path_raster)
l = 1
for j in list_path_raster:
    field_cl = 'NDVI_' + str(l)
    lulc.update_shapefile(args.input,j,x,y,fc,field_cl)
    print("Done raster: ", l )
    l = l + 1