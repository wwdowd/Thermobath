setwd("C:/dowdlabscripts")

datfile1 = "TigBath01_record.csv" 
datfile2 = "TigBath02_record.csv"
#datfile = file.choose() #lets you interactively choose file

#no line of metadata in our files
#fileMeta = scan(datfile, what = character(), sep = ',', nlines = 1)

df1 = read.csv(datfile1, sep = ',',header = F)  #,skip=1) #to skip first line
df2 = read.csv(datfile2, sep = ',',header = F)
library(plotrix)
###############################################################################
# Plot the data in 2-D plots
#plot only last 2 days or so, 3 readings per minute on average = 4320 per day
#col 3 is data read from bath
dateplot1 = df1$V1
bathplot1 = df1$V3
if (length(df1$V1) > 8640) {
   dateplot1 = df1$V1[end-8640:end]
   bathplot1 = df1$V3[end-8640:end]
} 

dateplot2 = df2$V1
bathplot2 = df2$V2
if (length(df2$V1) > 8640) {
  dateplot1 = df2$V1[end-8640:end]
  bathplot1 = df2$V3[end-8640:end]
} 

#set up plotting parameters
#mfcol = columnwise, mfrow = rowrise (LtoR first)
par(mfrow=c(2,4))
# X vs Y
plot(dateplot1, bathplot1, type = 'p', axis.Date(x),  title = 'Bath01',
     #		xlim = c(-1,1),
     #		ylim = c(-1,1),
     asp = 1,
     las = 1)

plot(dateplot2, bathplot2, type = 'p', xlabel = 'Bath01',
     #		xlim = c(-1,1),
     #		ylim = c(-1,1),
     asp = 1,
     las = 1)
