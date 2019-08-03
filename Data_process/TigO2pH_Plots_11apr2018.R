#setwd("C:/Source1") 
#set working directory to the file that contains all the .csv files for that water source.

filenames <- list.files(full.names=TRUE)
All <- lapply(filenames,function(i){
  read.csv(i,header=TRUE)
})
df <- do.call(rbind.data.frame, All)

df$Date <-as.POSIXct(df$date_time)

#install.packages("ggplot2")
#install.packages("gridExtra")

library(ggplot2)
library(gridExtra)

pH <- ggplot(data = df, aes(y = pH,x =Date))+
  geom_point()+
  theme_bw()+ 
  ylab("pH")+
  xlab("Date (MM DD)")+
  ggtitle("pH")

O2 <- ggplot(data = df, aes(y = O2_mgL,x =Date))+
  geom_point()+
  theme_bw()+ 
  ylab("O2 mg/L")+
  xlab("Date (MM DD)")+
  ggtitle("Oxygen")

grid.arrange(pH, O2, ncol=2, nrow =1)
