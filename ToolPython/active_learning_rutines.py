#====================================
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import fetch_mldata
from sklearn.preprocessing import MinMaxScaler  #StandardScaler
from sklearn.svm import SVC
import os
import Active_learning as al
import numpy as np
from osgeo import gdal, ogr
import pandas as pd

#====================================
# "training_samples3.shp"

folder_path = '/home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST_Filter'
list_folder_path = [os.path.join(folder_path , i) for i in os.listdir(folder_path)]
list_folder_path.sort()
for i in list_folder_path:
    path_shape = os.path.join(i,"training_samples6.shp")
    dataset = al.import_data(path_shape)
    dataset["data"] = dataset["data"].iloc[:,1:]
    print(dataset["data"])

    #clf = al.SvmModel()#
    clf = al.rf_model()
    (weights, entropies_df) = al.entropy_accumulation(dataset, clf, pivot = 'CLASS_NAME', prob =0.7, number_simulations = 200)
    print(weights)
    #
    #saving weigths000
    file_csv = os.path.join(i,"weights_training_samples6_rf.csv")
    entropies_df_t = entropies_df.T
    entropies_df_t.to_csv(file_csv, sep='\t')

    df_entropy = pd.DataFrame(weights , columns = ["weights"])
    df0 = pd.concat([dataset["data"],df_entropy], axis =  1)

    print(df0.dtypes)

    val = {}
    val["coordinates"] = dataset["coordinates"]
    val["data"] = df0
    val["proj"] = dataset["proj"]
    dsn = os.path.join(i,"training_samples6_rf_w.shp")
    #dsn = '/home/user/Documents/TESISMASTER/VECTOR/Training_data_composites/Summer/training_samples3_w_rf.shp'
    al.write_shapefile(val, dsn)
    val = None
    entropies_df_t = None
    weights = None
    print(f"This path : {i} is done")
