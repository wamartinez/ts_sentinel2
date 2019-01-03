
library(sf)

file_name = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/VECTOR/Vector_Spring_composite/training_samples6_rf_w_queryB_75.shp"
file_out = "/home/user/Documents/TESISMASTER/IMAGES/TO_PROCESS_10m/Prediction/VECTOR/Vector_Spring_composite/training_samples6_rf_w_queryB_75_out.shp"

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