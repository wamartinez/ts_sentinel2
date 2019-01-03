#well after classying the images I realized that I was wrking with nly one part of the variability of the data, that is samplingself.
#I want in this attempt to nrmalize the imagery before performing any calculation
import os
import argparse
from sklearn.preprocessing import StandardScaler
from osgeo import gdal
import lulc
import numpy as np
#image processing
from scipy import misc
from scipy import ndimage

# --folder_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Composites_max_ndvi/Autumn_composite
# --output_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Compositer_max_ndvi_Filter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", help = "Folder wih the imagery")
    parser.add_argument("--output_path", help = "Output for the new imagery")
    args = parser.parse_args()
    print(args.folder_path)



#path of the rasters
list_raster = [i for i in os.listdir(args.folder_path) if i.endswith('.tiff') or i.endswith('.jp2')]
list_raster.sort()
print(list_raster)
#names of the rasters

#creating folder with the same name
foutput = os.path.join(args.output_path,args.folder_path.split("/")[-1])
os.mkdir(foutput)

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
    #gaussian filter
    blurred_band = ndimage.median_filter(band, size = 5)
    #path of the new image
    output = os.path.join(foutput, i)
    lulc.write_geotiff(output,blurred_band, gt, proj)
    print(f'{i} was created')
    band = None
    aster_dataset = None
