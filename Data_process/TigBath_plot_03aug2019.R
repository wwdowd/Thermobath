#setwd("C:/dowdlabscripts")
setwd("D:/My_documents/WSU/Experiments/Tigriopus/R code")
myFile <- choose.files(default = "", caption = "Select 1 or more TigBathXX files",multi = TRUE)#file.choose()

noFiles = length(myFile)

if (noFiles < 4) {
  par(mfrow=c(1,4))}
if (noFiles > 4) {}
    {par(mfrow=c(2,4))}
#datfile1 = "TigBath01_record.csv" 
#datfile2 = "TigBath02_record.csv"
#datfile = file.choose() #lets you interactively choose file

#no line of metadata in our files
#fileMeta = scan(datfile, what = character(), sep = ',', nlines = 1)

for (i in 1:noFiles) {
  df1 = read.csv(myFile[i], sep = ',',header = F)  #,skip=1) #to skip first line
  #df2 = read.csv(datfile2, sep = ',',header = F)
  #library(plotrix)
###############################################################################
# Plot the data in 2-D plots
#plot only last 2 days or so, 3 readings per minute on average = 4320 per day
#col 3 is data read from bath
  dateplot1 = df1$V1 #as.Date(df1$V1, format = "%Y-%m-%d hh:mm:ss")
  bathplot1 = df1$V3
# if (length(df1$V1) > 8640) {
#    dateplot1 = as.Date(df1$V1[end-8640:end], format = "%Y-%m-%d hh:mm:ss")
#    bathplot1 = df1$V3[end-8640:end]
# } 
  plot(dateplot1, bathplot1, type = 'p', xlab = myFile[i],
       #		xlim = c(-1,1),
       #		ylim = c(-1,1),
       asp = 1,
       las = 1,
       axis.POSIXct(1, dateplot1, format = "%m-%d h",las = 2)) 
}
  
  
#####STUFF BELOW HERE IS OLD VERSION#######################################
# dateplot2 = df2$V1 #as.Date(df2$V1, format = "%Y-%m-%d hh:mm:ss")
# bathplot2 = df2$V2
# # if (length(df2$V1) > 8640) {
# #   dateplot1 = as.Date(df2$V1[end-8640:end], format = "%Y-%m-%d hh:mm:ss")
# #   bathplot1 = df2$V3[end-8640:end]
# # } 
# 
# #set up plotting parameters
# #mfcol = columnwise, mfrow = rowrise (LtoR first)
# par(mfrow=c(2,4))
# # X vs Y
# plot(dateplot1, bathplot1, type = 'p', xlab = "Bath01",
#      #		xlim = c(-1,1),
#      #		ylim = c(-1,1),
#      asp = 1,
#      las = 1,
#      axis.POSIXct(1, dateplot1, format = "%m-%d h",las = 2)) 
# 
# 
# 
# plot(dateplot2, bathplot2, type = 'p', xlab = "Bath02",
#      #		xlim = c(-1,1),
#      #		ylim = c(-1,1),
#      asp = 1,
#      las = 1,
#      axis.POSIXct(1, dateplot1, format = "%m-%d h",las = 2))
# 
# #axis.POSIXct(dateplot1, 1, format = "%m-%d h",#at = seq(dateplot1[1250], dateplot1[1600], length.out=20),
# #          , las = 2)
