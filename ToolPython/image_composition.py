#Convert image inf sentinel 2 format to tiff format
#We assume tha your folder dataset only cotain images
#  --name_raster D:\TESISMASTER\IMAGES\COMPOSITIONS\IM20170927_Composition_10m.tiff
#  --dataset D:\TESISMASTER\IMAGES\TO_PROCESS

import argparse
from osgeo import gdal
import numpy as np
import os

#
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name_raster", help = "Name of the raster")
    parser.add_argument("--dataset", help = "Work directory")
    args = parser.parse_args()
    print(args.dataset)

#Import gdal and thus the image
#I want to import only certain images with the same spatial resolution
#Name_images = ['B02','B03','B04','B05','B06','B07','B8A','B11','B12','DEM','NDVI','SLOPE']

list_files = [os.path.join(args.dataset,f) for f in os.listdir(args.dataset) if f.endswith('.jp2') or f.endswith('.tiff')  ]

print('proccessing',list_files)

bands_data= []
for f in list_files:
    driver = gdal.Open(f)
    r_dataset = driver.GetRasterBand(1)
    band = r_dataset.ReadAsArray()
    bands_data.append(band)
    #Projection and geotransformation are part of the last layer, so I will overwrite the object
    gt = driver.GetGeoTransform()
    proj = driver.GetProjectionRef()

bands_data = np.dstack(bands_data)
print('Stacking layers')
print(bands_data[:,:,1])
print(bands_data.shape)

#==========================================
#Create driver where I will store the array
#==========================================
out_fn = os.path.join(args.dataset,args.name_raster)
print(out_fn)
rows, cols, n_bands = bands_data.shape

driver2 = gdal.GetDriverByName('GTiff')
outd_ds = driver2.Create(out_fn, rows, cols,n_bands, gdal.GDT_Float32)
outd_ds.SetGeoTransform(gt)
outd_ds.SetProjection(proj)

for j in range(1,n_bands+1):
    band_o = outd_ds.GetRasterBand(j)
    band_o.WriteArray(bands_data[:,:,j-1])
    band_o = None
outd_ds =None
print('Done')
