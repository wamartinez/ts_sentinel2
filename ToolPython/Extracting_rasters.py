#take a folder with different raster files and extract the pixels accorising with the area of certain polygon

#--rasters_input  /home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST_filter_size3/1_Spring
#--rasters_output  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/COMPOSITES/Autumn_composite
#--shapefile  /home/user/Documents/TESISMASTER/VECTOR/CartoBase/area_corte.shp


from osgeo import gdal, ogr
import os
import argparse
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rasters_input', help = 'folder input with the rasters')
    parser.add_argument('--rasters_output', help = 'folder ouput with the rasters')
    parser.add_argument('--shapefile', help = 'shapefile used for the clipping')
    args = parser.parse_args()
    print("start processing")

#=============================
#Importing shapefile
#=============================
driver = ogr.GetDriverByName('ESRI Shapefile')
data_source = driver.Open(args.shapefile)
layer = data_source.GetLayer()

#defining extension of the clip
box = layer.GetExtent()
print(box)

#=============================
#Importing rasters
#=============================
#imput
path_rasters = [i for i in os.listdir(args.rasters_input) if i.endswith('.tiff') or i.endswith('.jp2')]
path_rasters.sort()
print(path_rasters)

#output

for i in path_rasters:
    raster_data_source = gdal.Open(os.path.join(args.rasters_input,i))
    gt = raster_data_source.GetGeoTransform()
    inv_gt = gdal.InvGeoTransform(gt)
    #tranforming in raster coordinates box coordinates

    x0_p , y0_p = gdal.ApplyGeoTransform(inv_gt, box[0],box[3])
    x1_p , y1_p = gdal.ApplyGeoTransform(inv_gt, box[1],box[2])
    x0_p = int(x0_p)
    y0_p = int(y0_p)
    x1_p = int(x1_p)
    y1_p = int(y1_p)

    #extracting raster
    in_band = raster_data_source.GetRasterBand(1)
    data = in_band.ReadAsArray(x0_p, y0_p, abs(x1_p - x0_p + 1),abs(y1_p - y0_p + 1))
        #interpolating empty pixels
    #only replace per mean 0
    data[np.isnan(data)] = 0
    #print(data)
    #=============================
    #Clipping raster
    #=============================
    #creating empy output raster
    print(f'clipping raster: { i } ')
    out_driver = gdal.GetDriverByName('GTiff')
    out_ds = out_driver.Create(os.path.join(args.rasters_output,i),abs(x1_p-x0_p+1),abs(y1_p-y0_p+1),1,gdal.GDT_Float32)
    out_ds.SetProjection(raster_data_source.GetProjection())
    #setting new origin of coordinates
    x0, y0 = gdal.ApplyGeoTransform(gt,x0_p,y0_p)
    out_gt = list(gt)
    out_gt[0] = x0
    out_gt[3] = y0
    out_ds.SetGeoTransform(out_gt)
    #storing array
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(data)
    out_ds.FlushCache()
    raster_data_source = None
    data = 0
