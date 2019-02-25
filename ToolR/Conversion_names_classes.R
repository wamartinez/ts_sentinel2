
library(sf)

<<<<<<< HEAD
file_name = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/VECTOR/STATIC/IM_20170729/training_samples7_rf_w_queryA_80.shp"
file_out =  "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/VECTOR/STATIC/IM_20170729/training_samples7_rf_w_queryA_80_out.shp"

df = sf::read_sf(file_name)

label_classes = c("Eucalyptus_trees","Herbaceous","Sealed", "Non_vegetated","Holm_and_Cork_Trees","Coniferous_trees", "Wetlands",
                  "Water","Bushes_and_shrubs" )

k=1
l= 0
for(i in label_classes){
=======
file_name = "/home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST_filter_size3/2_Summer/training_samples6_rf_w_queryA_70.shp"
#file_out =  "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/VECTOR/COMPOSITES/4_Winter/training_samples6_rf_w_queryA_70_out.shp"

df = sf::read_sf(file_name)

k=1
l= 0
for(i in unique(df$CLASS_NAME)){
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
  ind = which(df$CLASS_NAME == i)
  df[ind,"CLASS_NAME"] = k
  l= c(l,i)
  k = k + 1
}

#sf::write_sf(df,file_out)
<<<<<<< HEAD
l


#===============================
#creating traing and test data
#===============================

file1 = '/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/training_samples7.shp'
library(sf)
#df1 = sf::read_sf(file1)

output_test =  NULL
output_train =  NULL
for(i in unique(df1$CLASS_NAME)){
  index = which(df1$CLASS_NAME == i)
  id_random = sample(c(1:length(index)),0.8*length(index))
  output_train = rbind(output_train, df1[index[id_random],])
  output_test = rbind(output_test, df1[index[-id_random],])
}

file_train = '/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/training_samples8.shp'
file_test = '/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/test_samples8.shp'

sf::write_sf(output_train,file_train)
sf::write_sf(output_test,file_test)


=======
l
>>>>>>> ac173c5f72d856c3a48e1b2c234e6bde1e2aa60f
