import argparse
import lulc
import os
##Importing shapefile
from osgeo import ogr, gdal, osr
import os
import numpy as np

#well the idea of this is reproduce the shapefiles with the information of the raster in automatic way

#list of shapefiles
<<<<<<< HEAD
files_vector= r'D:\TESISMASTER\VECTOR\Training_data_ImageryST\TEMP'
files_raster= r'D:\TESISMASTER\IMAGES\TO_PROCESS_10m\Images_ST\TEMP'

#list shapefiles
list_shapefiles = [os.path.join(files_vector,i,"training_samples11.shp") for i in os.listdir(files_vector)]
=======
files_vector= '/home/user/Documents/TESISMASTER/VECTOR/Traning_data_composites_max_ndvi_ST_SS_F3'
files_raster= '/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Composite_max_ndvi_ST_SS_Filter3'

#list shapefiles
list_shapefiles = [os.path.join(files_vector,i,"training_samples6.shp") for i in os.listdir(files_vector)]
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
list_shapefiles.sort()

#list of rasters
list_rasters = [os.path.join(files_raster,i) for i in os.listdir(files_raster)]
list_rasters.sort()
<<<<<<< HEAD
print(list_rasters)
=======
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f

for args_raster , args_input in zip(list_rasters,list_shapefiles):
    print(args_input, "----", args_raster)
    #here I start with the usual script
    driver = ogr.GetDriverByName('ESRI Shapefile')
    datasource = driver.Open(args_input)
    #Get layer
    layer =  datasource.GetLayer()
    fc = layer.GetFeatureCount()
    proj_input = layer.GetSpatialRef()
    layer_defn = layer.GetLayerDefn()
    count_field = layer_defn.GetFieldCount()
<<<<<<< HEAD
    #Getting name of the fiels of the Shapefile
=======

    #Getting name of the fiels of the Shapefile

>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
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
    #Diigital elevation model

<<<<<<< HEAD
    dem_path = r'D:\TESISMASTER\ZDEM\IM_2017_ZDEM_10m.tiff'
    slope_path = r'D:\TESISMASTER\ZDEM\IM_2017_ZSLOPE_10m.tiff'
=======
    dem_path = "/home/user/Documents/TESISMASTER/ZDEM/IM_2017_ZDEM_10m.tiff"
    slope_path = "/home/user/Documents/TESISMASTER/ZDEM/IM_2017_ZSLOPE_10m.tiff"
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f

    list_path_raster = [os.path.join(args_raster,w) for w in os.listdir(args_raster) if w.endswith('.jp2') or w.endswith('.tiff')]
    list_path_raster.sort()
    list_path_raster.append(dem_path)
    list_path_raster.append(slope_path)
    print(list_path_raster)

    #creating name columns according with the name of the files

    list_names_raster = [w.split('.')[0].split("_")[-2] for w in os.listdir(args_raster) if w.endswith('.jp2') or w.endswith('.tiff')]
    list_names_raster.sort()
    list_names_raster.append("ZDEM")
    list_names_raster.append("ZSLOPE")
    print(list_names_raster)

    print("list of rasters")
    print(list_path_raster)
    l = 0
    for j in list_path_raster:
        field_cl = list_names_raster[l]
        lulc.update_shapefile(args_input,j,x,y,fc,field_cl)
        print("Done raster: ", list_names_raster[l] )
        l = l + 1
    datasource = None
    print(f'Done:::::::: {args_input}')
