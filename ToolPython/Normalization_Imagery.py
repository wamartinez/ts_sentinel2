#well after classying the images I realized that I was wrking with nly one part of the variability of the data, that is samplingself.
#I want in this attempt to nrmalize the imagery before performing any calculation
import os
import argparse
from sklearn.preprocessing import StandardScaler
from osgeo import gdal
import lulc
import numpy as np
from scipy import misc

<<<<<<< HEAD
# --folder_path  D:\TESISMASTER\IMAGES\TO_PROCESS_10m\Images\IM_20150725
# --output_path  D:\TESISMASTER\IMAGES\TO_PROCESS_10m\Images_ST\IM_20150725
=======
# --folder_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Composite_max_ndvi_SS_Filter3/SS_Composite
# --output_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Composite_max_ndvi_ST_SS_Filter3
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", help = "Folder wih the imagery")
    parser.add_argument("--output_path", help = "Output for the new imagery")
    args = parser.parse_args()
    print(args.folder_path)



#path of the rasters
<<<<<<< HEAD
list_raster = [i for i in os.listdir(args.folder_path) if i.endswith('.tiff') or i.endswith('.jp2') or i.endswith('.tif')]
=======
list_raster = [i for i in os.listdir(args.folder_path) if i.endswith('.tiff') or i.endswith('.jp2')]
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
list_raster.sort()
print(list_raster)
#names of the rasters

<<<<<<< HEAD
=======
#creating folder with the same name
foutput = os.path.join(args.output_path,args.folder_path.split("/")[-1])
os.mkdir(foutput)

>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
bands_data = []
for i in list_raster:
    #adding complete path
    input = os.path.join(args.folder_path,i)
    raster_dataset = gdal.Open(input , gdal.GA_ReadOnly)
    #geotransformation
    gt = raster_dataset.GetGeoTransform()
    proj = raster_dataset.GetProjectionRef()
    #Importing bands as a set of arrays
    n_bads = raster_dataset.RasterCount
    band =  raster_dataset.GetRasterBand(1).ReadAsArray()
    #calculation of mean
    mean = np.nanmean(band)
    #calculation of standard deviation
    std = np.nanstd(band)
    band_st = (band - mean)/std
    #path of the new image
<<<<<<< HEAD
    output = os.path.join(args.output_path,i)
=======
    output = os.path.join(foutput, i)
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
    lulc.write_geotiff(output,band_st, gt, proj)
    print(f'{i} was created')
    band = None
    aster_dataset = None
