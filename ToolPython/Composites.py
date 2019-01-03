#The attempt of this script is to get the image composites
import argparse
import os
import numpy as np
from osgeo import ogr, gdal
import lulc

#### --input  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Composites_max_ndvi/Winter_composite
#### --output /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Composites_max_ndvi/result

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
    list_file = [os.path.join(k,l) for l in os.listdir(k) if l.endswith(".jp2") or l.endswith(".tiff")]
    list_file.sort()
    list_files.append(list_file)

list_files_array = np.array(list_files)
print(list_files_array[:,10])

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
bands_ndvi = None
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
#robust analysis based in medians
#============================================

#def argmedian(x):
#    x1 = [i for i in x if str(i) != 'nan']
#    arg_median = np.argsort(x)[len(x1)//2]
#    return(arg_median)

#index_row_max = np.apply_along_axis(argmedian, 0, ndvi)
#============================================
#slicing maximum pixels of NDVI and getting indices
#reshaping index
vector_index = index_row_max.reshape(-1)
#reshaping ndvi
vector_bands = ndvi.reshape((times,cols*rows))
#slicing ndvi according with index
slice_max_band = vector_bands[vector_index,range(0,cols*rows)]
vector_bands = None
#returning two dimensions
new_ndvi = slice_max_band.reshape((cols,rows))
bands_ndvi = None
slice_max_band = None
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
        source = None
        band = None
    #stacking bands
    array_data = np.stack(bands_data)
    reshape_array_data = array_data.reshape((times,cols*rows))
    array_data = None
    #slicing  according with index
    selection_band_pixel = reshape_array_data[vector_index,range(0,cols*rows)]
    reshape_array_data = None
    #returning two dimensions
    new_band = selection_band_pixel.reshape((cols,rows))
    out_file = os.path.join(args.output, "Composition_Band" + str(i) + "_10m.tiff")
    lulc.write_geotiff(out_file,new_band, gt, proj)
    print('It was written the Band ' , i)
    bands_data = None
    selection_band_pixel = None
    new_band = None

print('Done')
