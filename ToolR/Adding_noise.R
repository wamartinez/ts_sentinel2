library(sf)


#classes = c("Herbaceous", "Sealed", "Non_vegetated","Wetlands", "Water","Woody" )

classes = c("Herbaceous","Sealed","Non_vegetated", "Wetlands","Water","Bushes_and_shrubs" , "Holm_and_Cork_Trees","Eucalyptus_trees","Coniferous_trees")



iterations = seq(from=40,to =740,by= 40)

for(l in iterations){
  file_shp = '/home/user/Documents/TESISMASTER/VECTOR/Training_data_ImageryST/TEMP/IM_20171216/training_samples8.shp'
  df_shp = sf::read_sf(file_shp)
  #create new column
  df_shp$CLASS_NAME2 = df_shp$CLASS_NAME
  output = NULL
  for(i in 1:9){
    index = which(df_shp$CLASS_NAME2 == classes[i])
    ind_random = sample(c(1:length(index)), l)  #240
    df_random = df_shp[index[ind_random],]
    df_norandom = df_shp[index[-ind_random],]
    #adding noise   #240
    for(j in 1:l){
      random_class = classes[sample(c(1:9)[-i],1)]
      df_random[j,"CLASS_NAME"] = random_class
    }
    #merging dataset
    df_final = rbind(df_norandom,df_random)
    output = rbind(output, df_final)
  }
  #table(output$CLASS_NAME)
  #table(output$CLASS_NAME2)
  file_out = paste0('/home/user/Documents/TESISMASTER/VECTOR/Noise/20171216/Noise_6_classes/training_samples8_Noise',l,'.shp')
  sf::write_sf(output[,-c(1,16)],dsn = file_out)
}

























