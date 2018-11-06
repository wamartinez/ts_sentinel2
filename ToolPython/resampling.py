#This script attempts to document the process of how do resampling and mask of one Image

#  --input   /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Spring/IM_20170115/IM_20170115_B05_20m.jp2
#  --source /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Spring/IM_20170115/IM_20170115_NDVI_10m.tiff
#  --output /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Spring/IM_20170115/IM_20170115_B05_10m.tiff

#Importing libraries
import argparse
from osgeo import gdal, ogr
import numpy as np
import os

#parsing
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help = 'path of the image that is target of resampling')
    parser.add_argument('--source', help = 'Image used as source to do the resampling')
    parser.add_argument('--output', help = 'path of the new raster')
    args = parser.parse_args()
    print('resampling')

#input
raster_dataset_input = gdal.Open(args.input)
gt_input = raster_dataset_input.GetGeoTransform()
prj_input = raster_dataset_input.GetProjectionRef()


#source of the especifications
raster_dataset_source = gdal.Open(args.source)
gt_source = raster_dataset_source.GetGeoTransform()
prj_source = raster_dataset_source.GetProjectionRef()
wide = raster_dataset_source.RasterXSize
high = raster_dataset_source.RasterYSize


#output
raster_dataset_output = gdal.GetDriverByName('GTiff').Create(args.output, wide, high, 1, gdal.GDT_Float32)
raster_dataset_output.SetGeoTransform(gt_source)
raster_dataset_output.SetProjection(prj_source)

#resampling
gdal.ReprojectImage(raster_dataset_input, raster_dataset_output, prj_input , prj_source, gdal.GRA_Bilinear)
del raster_dataset_output # Flush

print('Done!')
