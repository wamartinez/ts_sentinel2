#This script attempt to calculate NDVI
#I will assue that the raster has the red and the Nir in the third and seventh bands respectively

# --input_red  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Test/PC1_B_2.tiff
# --input_nir /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Test/PC1_B_6.tiff
# --output    /hom/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Test/IM_composite_NDVI_10m.tiff


import argparse
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_red', help = 'path of the red band')
    parser.add_argument('--input_nir', help = 'path of the nir band')
    parser.add_argument('--output', help = 'define the name and path of the NDVI in tiff format')
    args = parser.parse_args()
    print('processing ' +  args.output)

import gdal
import os


#importing red band
raster_dataset_red = gdal.Open(args.input_red)
gt = raster_dataset_red.GetGeoTransform()
proj =  raster_dataset_red.GetProjectionRef()

#importing near infrared band
#we assume that both bands have the same spatioal resolution
raster_dataset_nir = gdal.Open(args.input_nir)

#calculating NDVI
band_red = raster_dataset_red.GetRasterBand(1).ReadAsArray()
band_nir = raster_dataset_nir.GetRasterBand(1).ReadAsArray()
#array_ones = np.ones(band_red.shape)
nu = band_nir.astype(float) - band_red.astype(float) #+ array_ones
de = band_nir.astype(float) + band_red.astype(float) #+ array_ones
ndvi_array = nu /de

#Exporting results
rows, cols = ndvi_array.shape
driver2 =  gdal.GetDriverByName('GTiff')

out_ds = driver2.Create(args.output, rows, cols, 1, gdal.GDT_Float32)
out_ds.SetGeoTransform(gt)
out_ds.SetProjection(proj)
band_o = out_ds.GetRasterBand(1)
band_o.WriteArray(ndvi_array)
band_o = None
out_ds =None
print('Done')
