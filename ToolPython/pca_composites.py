#pca to construct composites
#I want to implemernt principal components per band and per season, so that I
#I can compore thoseresults with the methodology of maximun ndvi
#I will retrieve only the firsr component of the analysis
# --raster_path /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Autumn
# --out_path  /home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Composites_pca/Autumn
import argparse
import numpy as np
import os
from osgeo import gdal
import lulc

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raster_path',help='imput data path')
    parser.add_argument('--out_path',help='output path')
    args = parser.parse_args()
    print('start processing')

#function of normalization
def normalization(x):
    mean_x = np.nanmean(x)
    std_x = np.nanstd(x,ddof = 1)
    z = np.divide(x - mean_x,std_x)
    return z

def principal_components(y):
    row, col = y[0].shape
    n_samples = row * col
    index_samples = np.random.choice(n_samples, size=100000, replace=False)
    y_query_list = []
    y_norm_list = []
    w = 0
    for i in y:
        vector_y = i.reshape(-1)
        y_band_norm = normalization(vector_y)
        y_norm_list.append(y_band_norm)
        y_query_list.append(y_band_norm[index_samples])
        print(f'Band {w}')
        w = w + 1
    y_stack = np.array(y_norm_list)
    y_query_stack = np.array(y_query_list)
    V = np.cov(y_query_stack)
    values, vectors = np.linalg.eig(V)
    P1 = np.matmul(vectors.T,y_stack)[0]
    PC1_band = P1.reshape((row,col))
    stack_b = None
    y_stack = None
    y_query_stack = None
    P1 = None
    return PC1_band

list_folder = [os.path.join(args.raster_path,i) for i in os.listdir(args.raster_path)]
#list with the folders
list_folder.sort()
number_folders = len(list_folder)
print(f'processing {number_folders} folders')
#list with the files inside the folders
list_folder_file = []
for k in list_folder:
    a = [os.path.join(k,j) for j in os.listdir(k) if j.endswith('jp2') or j.endswith('tiff')]
    a.sort()
    list_folder_file.append(a)
#SO organizing folders with only one type of band per list
number_images_folder = len(list_folder_file[0])
new_list_folder_file = []
for k in range(0, number_images_folder):
    a = []
    for w in range(0,number_folders):
        a.append(list_folder_file[w][k])
    new_list_folder_file.append(a)

print(new_list_folder_file[10])


##================================
#Principal components
##================================
#since the imagery here is huge, I will construct the var-cov from a random n_samples

#Importing imagery
for h in range(0, number_images_folder):
    print(f'processing bands {h}')
    bands_pband = []
    for i in new_list_folder_file[h]:
        raster_dataset = gdal.Open(i, gdal.GA_ReadOnly)
        gt = raster_dataset.GetGeoTransform()
        proj = raster_dataset.GetProjectionRef()
        band =  raster_dataset.GetRasterBand(1)
        band_array = band.ReadAsArray()
        row, col = band_array.shape
        bands_pband.append(band_array)
        print(f'Imported: {i}')
        raster_dataset = None
    pc1 = principal_components(bands_pband)
    namefile = "PC1_B0"+ str(h) + ".tiff"
    out_file = os.path.join(args.out_path,namefile)
    lulc.write_geotiff(out_file,pc1, gt, proj)
    pc1 = None

print('Done')
