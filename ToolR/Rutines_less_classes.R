

library(sf)
file = '/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/training_samples7.shp'
df = sf::read_sf(file)


query_woody = df[df$CLASS_NAME %in% c('Holm_and_Cork_Trees', 'Eucalyptus_trees', 'Coniferous_trees','Bushes_and_shrubs'),]

random_index = sample(c(1:dim(query_woody)[1]),1000)
       
random_query_woody = query_woody[random_index,] 

random_query_woody$CLASS_NAME = 'Woody'

no_woody = df[!(df$CLASS_NAME %in% c('Holm_and_Cork_Trees', 'Eucalyptus_trees', 'Coniferous_trees','Bushes_and_shrubs')),]

newdf = rbind(no_woody, random_query_woody)

dim(newdf)
#creating test data
output_train = NULL
output_test = NULL
for(i in unique(newdf$CLASS_NAME)){
  index = which(newdf$CLASS_NAME == i)
  random_index_nd = sample(c(1:1000),300)
  df_test = newdf[index[random_index_nd],]
  output_test = rbind(output_test, df_test)
  df_train = newdf[index[-random_index_nd],]
  output_train = rbind(output_train, df_train)
}

file_out_train = paste0('/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/training_samples11.shp')
file_out_test = paste0('/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/test_samples11.shp')
sf::write_sf(output_train, dsn = file_out_train)
sf::write_sf(output_test, dsn = file_out_test)








