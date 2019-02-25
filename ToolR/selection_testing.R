library(sf)

file_out = '/home/user/Documents/TESISMASTER/VECTOR/Testing/Testing_samples.shp'


######

#intersecting


file_path_spring = '/home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST/Spring_composite/training_samples7_rf_w_queryB_60.shp'
file_path_summer = '/home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST/Summer_composite/training_samples7_rf_w_queryB_60.shp'
file_path_autumn = '/home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST/Autumn_composite/training_samples7_rf_w_queryB_60.shp'
file_path_winter = '/home/user/Documents/TESISMASTER/VECTOR/Training_data_composites_max_ndvi_ST/Winter_composite/training_samples7_rf_w_queryB_60.shp'

df_spring = sf::read_sf(file_path_spring)
df_summer = sf::read_sf(file_path_summer)
df_autumn = sf::read_sf(file_path_autumn)
df_winter =  sf::read_sf(file_path_winter)

df1 = sf::st_intersection(df_spring[,"CLASS_NAME"],df_summer[,"CLASS_NAME"])
df2 = sf::st_intersection(df1,df_autumn[,"CLASS_NAME"])
df3 = sf::st_intersection(df2,df_winter[,"CLASS_NAME"])
dim(df3)
table(df3$CLASS_NAME)


#random selection
df0 = NULL
for(i in unique(df3$CLASS_NAME)){
  index = which(df3$CLASS_NAME == i)
  id_random = sample(1:(length(index)),40)
  df0 = rbind(df0, df3[index[id_random],])
}

df_final = df0[,"CLASS_NAME"]

#sf::write_sf(df_final,file_out)






















