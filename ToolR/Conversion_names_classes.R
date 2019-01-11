
library(sf)

file_name = "/home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST_filter_size3/2_Summer/training_samples6_rf_w_queryA_70.shp"
#file_out =  "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/VECTOR/COMPOSITES/4_Winter/training_samples6_rf_w_queryA_70_out.shp"

df = sf::read_sf(file_name)

k=1
l= 0
for(i in unique(df$CLASS_NAME)){
  ind = which(df$CLASS_NAME == i)
  df[ind,"CLASS_NAME"] = k
  l= c(l,i)
  k = k + 1
}

#sf::write_sf(df,file_out)
l