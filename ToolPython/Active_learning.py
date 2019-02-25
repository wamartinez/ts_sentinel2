#==================================
# ACTIVE LEARNING RUTINE
#==================================

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import fetch_mldata
from sklearn.preprocessing import MinMaxScaler  #StandardScaler
from sklearn.svm import SVC
import os
import numpy as np
from osgeo import gdal, ogr
import pandas as pd

#====================================

#importing shapefile

def import_data(path_shape):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.Open(path_shape)
    layer = data_source.GetLayer()
    layer_defn = layer.GetLayerDefn()
    count_field = layer_defn.GetFieldCount()
    print(layer_defn.GetFieldDefn(0).GetType)
    fc = layer.GetFeatureCount()  # number of rows
    proj = layer.GetSpatialRef()  #projection
    #Getting name of the fields of the Shapefile
    schema = []
    #variables
    for k in range(0,count_field):
        f_field = layer_defn.GetFieldDefn(k)
        schema.append(f_field.name)
    #importing features
    x = []
    y = []
    data = []
    coordinates = []
    sp_obj = {}
    for feat in layer:
        #coordinates
        pt = feat.geometry()
        coord_par = [pt.GetX(),pt.GetY()]
        coordinates.append(coord_par)
        #variables
        fields = []
        for i in range(0, count_field):
            f = feat.GetField(i)
            fields.append(f)
        #second part
        data.append(fields)
    #array of data in data frame format
    #for string
    dataset = pd.DataFrame(data,columns = schema)
    #coordinates
    coord_df = pd.DataFrame(np.array(coordinates),columns = ["x","y"])
    sp_obj = {
    "coordinates":coord_df,
    "data":dataset,
    "proj":proj
    }
    #returning object
    return(sp_obj)

class random_selection:
    def __init__(self, dataset, prob, pivot):
        self.dataset = dataset
        self.prob = prob
        self.pivot = pivot

    def stratified_random_selection(self):
        #empty spatial object
        dataset_c = self.dataset
        prob = self.prob
        sp_obj_train = {}
        sp_obj_test = {}
        #classes
        classes = np.unique(dataset_c["data"][self.pivot].values)
        ind_train = []
        ind_test = []
        for i in classes:
            ind = np.where(dataset_c["data"][self.pivot].values == i)[0]
            n_id = int(len(ind)*prob)    #percentage of points to select
            ri = np.random.choice(ind, len(ind), replace=False).tolist()
            ind_train = ind_train + ri[:n_id]
            ind_test = ind_test + ri[n_id:]
        #subsetting training
        sp_obj_train = {
            "coordinates":dataset_c["coordinates"].loc[ind_train],
            "data":dataset_c["data"].loc[ind_train],
            "proj":dataset_c["proj"]
            }
        #subsetting test
        sp_obj_test = {
            "coordinates":dataset_c["coordinates"].loc[ind_test],
            "data":dataset_c["data"].loc[ind_test],
            "proj":dataset_c["proj"]
            }
        return (sp_obj_train , sp_obj_test)
#====================================
class SvmModel():
    model_type = 'Support Vector Machine with linear Kernel'
    def fit_predict(self, X_train, y_train, X_test):
        print ('training svm...')
        self.classifier = SVC(C=4, kernel = 'rbf',gamma= 0.25, probability=True)
        self.classifier.fit(X_train, y_train)
        self.test_y_predicted = self.classifier.predict(X_test)
        self.probability_y = self.classifier.predict_proba(X_test)
        return(self.test_y_predicted,self.probability_y)

#====================================

class rf_model():
    model_type  = 'Random forest'
    def fit_predict(self, X_train, y_train, X_test):
        print('Training random forest')
        self.classifier = RandomForestClassifier(n_estimators = 100)
        self.classifier.fit(X_train,y_train)
        self.test_y_predicted = self.classifier.predict(X_test)
        self.probability_y = self.classifier.predict_proba(X_test)
        #self.val_y_predicted = self.classifier.predict(X_val)
        return(self.test_y_predicted,self.probability_y)

#====================================

class Normalize():
    def normalize(self, X_train, X_test):
        self.scaler = MinMaxScaler()
        X_train = self.scaler.fit_transform(X_train)
        X_test  = self.scaler.transform(X_test)
        return (X_train, X_test)

#====================================
class measureselection():
    def EntropySelection(self, probabilities):
        def entropyfunc(x):
            ind = np.where(x != 0)[0]
            e = (x[ind] * np.log2(x[ind])).sum()
            return(e)
        #implementing function
        self.entropy = np.apply_along_axis(entropyfunc, 1, probabilities)
        return(self.entropy)

#====================================

def write_shapefile(dict_spatial, dsn):
    driver2 = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(dsn):
        print('Deleting')
        driver2.DeleteDataSource(dsn)
    point_datasource =  driver2.CreateDataSource(dsn)
    points_layer = point_datasource.CreateLayer('output',dict_spatial['proj'], geom_type =  ogr.wkbPoint)
    #colnames
    sch = dict_spatial['data'].dtypes.index.tolist()
    schema = [str(i) for i in sch]
    print(schema)
    schema_type = dict_spatial['data'].dtypes
    #create field
    for i ,j in zip(schema,schema_type):
        if j == np.dtype(np.int64) or j == np.dtype(np.float64):
            field = ogr.FieldDefn(i, ogr.OFTReal)
            points_layer.CreateField(field)
        else:
            field = ogr.FieldDefn(i, ogr.OFTString)
            points_layer.CreateField(field)
    #loading coordinates
    rows, col = dict_spatial['data'].shape
    #set indeces
    #dict_spatial['data'].reset_index
    for i in range(0,rows):
        #create points
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(dict_spatial['coordinates'].iloc[i,0],dict_spatial['coordinates'].iloc[i,1])
        #Create features
        feat = ogr.Feature(points_layer.GetLayerDefn())
        feat.SetGeometry(point)
        #Add fields of the input shapefile
        for k in sch:
            feat.SetField(str(k),dict_spatial['data'][k].values[i])
        points_layer.CreateFeature(feat)
        feat = None
    print("done")


def entropy_accumulation(dataset, clf, pivot, prob, number_simulations = 10):
    print("Start calculation of weigths")
    rows,cols = dataset["data"].shape
    c = []
    for i in range(0, number_simulations):
        print(f"Iteration {i}")
        random = random_selection(dataset, prob, pivot)
        (train,test) = random.stratified_random_selection()
        y_train = train["data"][pivot].values
        X_train = train["data"].iloc[:,1:].values
        #inste of calling the validation, I will import all the data for validation
        X_test = dataset["data"].iloc[:,1:].values
        #fitting model
        (label_pred , probabilities) =  clf.fit_predict(X_train,y_train, X_test)
        #calculaing entropies
        obj_entropy = measureselection()
        result_entropies = obj_entropy.EntropySelection(probabilities)
        #store entropies in a list
        c.append(result_entropies)
    entropies_stack = np.stack(c)
    entropies_df = pd.DataFrame(entropies_stack)
    #print(entropies_df)
    entropies = np.apply_along_axis(np.median,0,entropies_df)
    #Normalizing entropy min max according with the list_classes
    min_x = -3.3220#entropies.min()
    max_x =  0#entropies.max()
    m = 1/(max_x-min_x)
    b = 1 - m * max_x
    entropies = entropies * m + b
    return(entropies, entropies_df )
    print("done")


#this is part of a second a ttempt to see if the removing of outliers must be per iteration and not by labelling as it was done before


def entropy_rutines(train , clf, pivot):
    print("Start process")
    #calling train
    y_train = train["data"][pivot].values
    X_train = train["data"].iloc[:,1:].values
    #fitting model for itself
    (label_pred , probabilities) =  clf.fit_predict(X_train, y_train, X_train)
    #calculating entropies
    obj_entropy = measureselection()
    result_entropies = obj_entropy.EntropySelection(probabilities)
    train = None
    test1 = None
    return(result_entropies)
    #entropies_df = pd.DataFrame(entropies_stack)
    return(entropies, entropies_df )
    print("done")
