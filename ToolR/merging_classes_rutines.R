#===========================
#merging some classes
#===========================


library(sf)
filename = '/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/training_samples.shp'
df = sf::read_sf(filename)

#========================================================
#Separating dataset form vineyard orchards and olive trees
#========================================================

DF0 = df[!(df$CLASS_NAME %in% c("Vineyard","Orchards", "Olive_trees")), ]

#file_out = '/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/training_samples2.shp'

#sf::write_sf(DF0, dsn = file_out)

###=============================================================
#Herbaceous periodic, herbaceous permanent and natural herbaceus
###=============================================================
DF1 = DF0[DF0$CLASS_NAME %in% c("Herbaceous_periodic","Herbaceous_permanet"),]
DF1_e = DF0[!(DF0$CLASS_NAME %in% c("Herbaceous_periodic","Herbaceous_permanet","Natural_Herbaceous")),]

#selecting randomly 1000 samples, being fair with each classs
id_m = 0
for(i in unique(DF1$CLASS_NAME)){
  idx = which(DF1$CLASS_NAME == i)
  id1 =sample(c(1:1000),500)
  id_m = c(id_m, idx[id1])
}
id_t = id_m[-1] 

DF2_query = DF1[id_t,]
table(DF2_query$CLASS_NAME)
#new name
DF2_query$CLASS_NAME = "Herbaceous"

DF2 = rbind(DF2_query, DF1_e)

#writing

file_out_n = '/home/user/Documents/TESISMASTER/VECTOR/Raw_trainingdata/training_samples6.shp'

sf::write_sf(DF2, dsn = file_out_n)

























