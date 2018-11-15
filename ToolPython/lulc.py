
from osgeo import gdal, ogr
import numpy as np
import matplotlib.pyplot as plt
import itertools
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def create_mask_from_vector (vector_data_path, cols, rows, geo_transform, projection, target_value=1):
    """Rasterize the given vector(wrapper for gdal.RasterizeLayer)."""
    data_source= gdal.OpenEx(vector_data_path, gdal.OF_VECTOR)
    layer= data_source.GetLayer(0)
    driver= gdal.GetDriverByName('MEM')
    target_ds= driver.Create('',cols,rows,1,gdal.GDT_UInt16)
    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(projection)
    gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[target_value])
    return target_ds



def vectors_to_raster(file_paths, rows, cols, geo_transform, projection):
    """Rasterize all the vectors in the given directory into a single image. """
    labeled_pixels = np.zeros((rows, cols))
    for i, path in enumerate(file_paths):
        label = i+1
        ds= create_mask_from_vector(path,cols, rows,geo_transform,projection,target_value=label)
        band=ds.GetRasterBand(1)
        labeled_pixels += band.ReadAsArray()
        ds=None
    return labeled_pixels


def stratified_sampling(training_labels, prob):
    train_vector = []
    test_vector = []
    for i in np.unique(training_labels):
        index = np.where(np.array(training_labels) == i)[0]
        n_samples = len(index)
        random_vector = np.random.choice(n_samples, size=n_samples, replace=False)
        tr = index[random_vector[0:int(prob[0]*n_samples)]]
        te = index[random_vector[int(prob[0]*n_samples)::]]
        train_vector = train_vector + tr.tolist()
        test_vector = test_vector + te.tolist()
    return train_vector, test_vector

#training_labels = ['1','1','2','2','3','3','1','1','2','2','3','3','1','1','2','2','3','3']
#tr, tes = stratified_sampling(training_labels)
#e
#======================================
#Tunning parameters
#======================================
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def tunning_parameters_RF(train_samples, train_labels, prob):
    #Selecting training and validation data
    trv , tesv = stratified_sampling(train_labels, prob)
    #train
    train_samples_v= train_samples[trv,]
    train_labels_v = train_labels[trv,]
    #validation
    validation_samples_v = train_samples[tesv,]
    validation_labels_v = train_labels[tesv,]
    #Defining size of the parameters
    split = list(range(3,7))
    trees = np.arange(10,300,10)
    #loop each element of every parameter
    list_accuracy = []
    for i in split:
        acc_score = []
        for j in trees:
            classifier= RandomForestClassifier(n_estimators = j,min_samples_split = i)
            classifier.fit(train_samples_v, train_labels_v)
            result = classifier.predict(validation_samples_v)
            acc_score.append(accuracy_score(result, validation_labels_v))
        list_accuracy.append(acc_score)
    #plotting
    #List of colors
    list_colors = ['b--','g--','r--','c--','m--','k--','y--']
    for k in range(0, len(split)):
        plt.plot(trees,list_accuracy[k],list_colors[k], label = split[k])
    plt.ylabel('Accuracy')
    plt.xlabel('Number of trees in the forest')
    plt.legend()
    plt.show()

#======================================
#Confusion matrix
#======================================

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    #print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()


#create the geotiff from an array
def write_geotiff(fname, data, geo_transform, projection):
    """Create a GeoTIFF file with the given data."""
    driver= gdal.GetDriverByName('GTiff')
    rows, cols= data.shape
    dataset= driver.Create(fname, cols, rows, 1, gdal.GDT_Float32 ) #  gdal.GTD_Byte
    dataset.SetGeoTransform(geo_transform)
    dataset.SetProjection(projection)
    band= dataset.GetRasterBand(1)
    band.WriteArray(data)
    dataset=None #Close the file
    print("done")

#function connected to extract raster to point
def update_shapefile(x_shapefile,x_raster,x,y,fc,field_cl):
    raster_dataset = gdal.Open(x_raster)
    #geotransformation parameters
    gt = raster_dataset.GetGeoTransform()
    #calling values in array format
    band = raster_dataset.GetRasterBand(1)
    band_data = band.ReadAsArray()
    #===============================
    #Intersecting raster and points
    #===============================
    #inverse of the geotransformation
    inv_gt = gdal.InvGeoTransform(gt)
    xt_p = []
    yt_p = []
    for k in range(0,fc):
        xt , yt = gdal.ApplyGeoTransform(inv_gt, x[k], y[k])
        xt_p.append(xt)
        yt_p.append(yt)
    #intersecting
    value = []
    for i in range(0,fc):
        value.append(band_data[int(yt_p[i]),int(xt_p[i])])

    #=========================
    #Updating output file
    #=========================
    #Set again driver
    driver2 = ogr.GetDriverByName('ESRI Shapefile')
    #OPen Shapefile in edit version
    points_datasource = driver2.Open(x_shapefile,1)
    layer2 =  points_datasource.GetLayer()
    points_datasource.SyncToDisk()
    new_field = ogr.FieldDefn(field_cl, ogr.OFTReal)
    layer2.CreateField(new_field)
    i= 0
    for fe in layer2:
        fe.SetField(field_cl,float(value[i]))
        layer2.SetFeature(fe)
        i = i + 1
    #destroy instance of the data data_source
    points_datasource = None
    del value
    fe = None
    print('done')



#===================================================================
#function pca
#===================================================================

def pca_calculator(w):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    datasource = driver.Open(w)
    layer = datasource.GetLayer()
    proj = layer.GetSpatialRef()
    layer_defn = layer.GetLayerDefn()
    count_field = layer_defn.GetFieldCount()

    #schema: name the of the columns
    schema = []
    for k in range(0,count_field):
        f_field = layer_defn.GetFieldDefn(k)
        schema.append(f_field.name)
    #importing features in a list
    f2 = []
    #Importing features
    for feat in layer:
        f1 = []
        for i in range(0, count_field):
            field = feat.GetField(i)
            f1.append(field)
        #second part
        f2.append(f1)

    #converting list to dataframe
    df=pd.DataFrame(f2,columns=schema)
    #==============================
    #PCA Analysis
    #==============================
    #subsettin only variables
    features = schema[2:]
    df_x = df.loc[:,features]
    #separating labels
    df_y = df.loc[:,"CLASS_NAME"]
    #scaling data frame x
    df_x_scale = StandardScaler().fit_transform(df_x)

    #setting number of components to retrieve
    pca = PCA(n_components = 2)
    #calculating pca
    pc_t = pca.fit_transform(df_x_scale)
    print(pc_t)
    print(pc_t.shape)
    #defining new data frame with first two composites
    df_x_pc = pd.DataFrame(data = pc_t, columns= ["pc1","pc2"])
    #concatening prirncipal components with explicative variables
    df_pc = pd.concat([df_y,df_x_pc], axis = 1)
    datasource = None
    return df_pc

#=====================================================================
