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
<<<<<<< HEAD
    dataset = al.import_data(os.path.join(i,"training_samples11_rf_w.shp"))
=======
    dataset = al.import_data(os.path.join(i,"training_samples6_rf_w.shp"))
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
    list_classes = np.unique(dataset["data"].CLASS_NAME.values)
    list_indeces = []
    for j in list_classes:
        index_class = np.where(dataset["data"].CLASS_NAME.values == j)[0]
        weights = dataset["data"].weights.values[index_class]
<<<<<<< HEAD
        threshold = int(len(index_class)*0.40)
=======
        threshold = int(len(index_class)*0.55) #45
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
        a = np.argsort(weights)
        ind = a[threshold:]
        query_ind = index_class[ind]
        list_indeces = list_indeces + query_ind.tolist()
        #print(query_ind)
    print(list_indeces)
    #queryng dataset
    sp_obj_test  = {}
    sp_obj_test = {
        "coordinates":dataset["coordinates"].loc[list_indeces],
        "data":dataset["data"].loc[list_indeces],
        "proj":dataset["proj"]
        }
<<<<<<< HEAD
    path_out = os.path.join(i,"training_samples7_rf_w_queryB_60.shp")
=======
    path_out = os.path.join(i,"training_samples6_rf_w_queryB_45.shp")
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
    al.write_shapefile(sp_obj_test, path_out)
    print(f"done {i}")
