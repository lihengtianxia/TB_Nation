
library(forecastxgb)
library(dplyr)
library(readxl)

setwd('~/DataScience/TB_Nation/XGBoost/')

tb <- read_excel('../Data/TB_nation.xlsx')

dta<- ts(tb[1:108,'Incidence_rate'],start = c(2005,1),frequency = 12)

model <- xgbar(dta)
summary(model)

fc <- forecast(model, h = 12)
plot(fc)

y_true <- tb$Incidence_rate[109:120]
y_pred <-  as.numeric(fc$mean)

comp <- data.frame(y_pred,y_true)
comp$error <- comp$y_pred - comp$y_true
comp$error <- abs(comp$y_pred - comp$y_true)
comp$error <- abs(comp$y_pred - comp$y_true)/comp$y_true*100
mean(comp$error)
