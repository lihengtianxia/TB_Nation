# Title: National TB Statistics
# Author: Evan Zhu
# Last modified: 16/8/1

library(readxl)
setwd('/Users/Evan/DataScience/TB_GM/National TB Statistics/')
directory <- '/Users/Evan/DataScience/TB_GM/National TB Statistics/'

# data import

# j control the area by substr the row
# year_start

data_import <- function(directory,j=1,year_start=1,year_end=10,skip=1){
        datasets <- data.frame()
        file_num= seq(year_start,year_end,1)
        for (i in file_num){
                data <- read_excel(list.files(directory,full.names=TRUE)[i],skip=skip)[j,1:5]
                data$year <-  substr(list.files(directory)[i],1,4)
                names(data) <-c('area','incidence','death','incidence rate','death rate','year')
                datasets <- rbind(datasets,data)
     }
   # write.csv(datasets,paste0('~/Desktop/data/nation_TB',j,'.csv'),fileEncoding='GB2312')
     write.csv(datasets,paste0('../data/nation_TB',j,'.csv'))
 }

# data_import(directory,j=1)

for (k in 1:33){
        data_import(directory,j=k,year_start=1,year_end=10)
}
