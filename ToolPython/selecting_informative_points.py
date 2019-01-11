#the attempt of this script is to select certain percentage of the data
#for the classsification, this selection is based in the results of entropy that ranges
#within 0 and 1
import numpy as np
import Active_learning as al
import os

file_folders = '/home/user/Documents/TESISMASTER/VECTOR/Training_data_ImageryST'
folder_list = [os.path.join(file_folders,i) for i in os.listdir(file_folders)]
folder_list.sort()

print(folder_list)

for i in folder_list:
    dataset = al.import_data(os.path.join(i,"training_samples6_rf_w.shp"))
    row, col = dataset["data"].shape
    weights = dataset["data"].loc[:,"weights"]
    threshold = int(row*0.15) #45
    a = np.argsort(weights)
    ind = a[threshold:]
    query_ind = ind.tolist()
    print(query_ind)
    #queryng dataset
    sp_obj_test  = {}
    sp_obj_test = {
        "coordinates":dataset["coordinates"].loc[query_ind],
        "data":dataset["data"].loc[query_ind],
        "proj":dataset["proj"]
        }
    path_out = os.path.join(i,"training_samples6_rf_w_queryA_85.shp")
    al.write_shapefile(sp_obj_test, path_out)
    print(f"done {i}")
