#The attempt of this script is to get the image composites
import argparse
import os
import numpy as np
from osgeo import ogr, gdal
import lulc

####  --input  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Summer
#### --output  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Summer_Composicion

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',help='path of the folder with the imagery')
    parser.add_argument('--output',help='path of the raster')
    args = parser.parse_args()
    print('processing ' + args.input)

#============================================
#creating list with the path of the imagery
#============================================
list_folder = [os.path.join(args.input,i) for i in os.listdir(args.input)]
list_folder.sort()

list_files = []
for k in list_folder:
    list_file = [os.path.join(k,l) for l in os.listdir(k)]
    list_file.sort()
    list_files.append(list_file)

list_files_array = np.array(list_files)
print(list_files_array)

#============================================
#NDVI selection
#============================================
#Importing ndvi
#ndvi paths, here band 3
ndvi_paths = list_files_array[:,10]
bands_ndvi = []
for i in ndvi_paths:
    ndvisource = gdal.Open(i)
    gt = ndvisource.GetGeoTransform()
    proj = ndvisource.GetProjectionRef()
    band =  ndvisource.GetRasterBand(1)
    bands_ndvi.append(band.ReadAsArray())
    ndvisource = None
#stacking layers of ndvi
ndvi = np.stack(bands_ndvi)
#definition of the shape of the array
times, cols, rows  = ndvi.shape
print(ndvi)
print(times)
print(cols)
print(rows)

#getting indeces of the largest ndvi in the axis time
#===========================================
#This was before, problems with memory
index_row_max = np.argmax(ndvi,0)
#============================================
#===========================================
#This is now jojojo
'''
def argmaximum(x):
    a = np.argmax(x)
    return a

index_row_max = np.apply_along_axis(argmaximum, 0, ndvi)
'''
#============================================
#slicing maximum pixels of NDVI and getting indices
#reshaping index
vector_index = index_row_max.reshape(-1)
#reshaping ndvi
vector_bands = ndvi.reshape((times,cols*rows))
#slicing ndvi according with index
slice_max_band = vector_bands[vector_index,range(0,cols*rows)]
#returning two dimensions
new_ndvi = slice_max_band.reshape((cols,rows))
print('Ready selection of maximum NDVI')
#===============================================
#Saving NDVI
#===============================================
out_file_ndvi = os.path.join(args.output,"Composition_ndvi.tiff")
lulc.write_geotiff(out_file_ndvi,new_ndvi, gt, proj)
print('it was written the ndvi file')

#===============================================
#Creating composites
#===============================================
print('Creating rest of the bands...')
number_im = len(list_files_array[0,:])
for i in range(0,number_im-1):
    bands_data=[]
    list_path_band = list_files_array[:,i]
    for j in list_path_band:
        source = gdal.Open(j)
        band =  source.GetRasterBand(1)
        bands_data.append(band.ReadAsArray())
    #stacking bands
    array_data = np.stack(bands_data)
    reshape_array_data = array_data.reshape((times,cols*rows))
    #slicing  according with index
    selection_band_pixel = reshape_array_data[vector_index,range(0,cols*rows)]
    #returning two dimensions
    new_band = selection_band_pixel.reshape((cols,rows))
    source = None
    out_file = os.path.join(args.output, "Composition_Band" + str(i) + ".tiff")
    lulc.write_geotiff(out_file,new_band, gt, proj)
    print('it was written the Band ' , i)

print('Done')
