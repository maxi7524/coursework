library(readxl)
#set working directory to the folder containing the material for
#the practical lessons through the command setwd("path to folder"),
#or Session>Set Working directory

# chunk 2 

A<-read_xlsx("BW25113_Growth_Round01.xlsx")
tms<-A$`Time (h)`
#I will use the first non-blank growth curve
od_ori<-A$Curve00013
#blanks (controls) are in columns 2-13
#we calculate the median across all control replicates, to be used to correct
#optical density measurements
#in reality the control are almost constant in time, so this
#correction has no effect on estimation of the slope
blk<-unlist(apply(A[,2:13],1,function(x)median(x,na.rm=T)))

#remove the control from optical density measurements
od<-od_ori - blk

#let's cut the period in which we have data and remove zeros
od<-od[tms<20]
tms<-tms[tms<20]
z<-which(od==0)
od<-od[-z]
tms<-tms[-z]
plot(tms,log(od),type="p",pch=18,cex=1.25)

# chunk 3

#in the paper associated to the data
#they calculate the growth rate using
# log10(od(t)/od(t-1)) / delta t
#delta t = t - (t-1)
#here intervals are all the same
#we replace delta t with 0.5 hours
mupaper<-log10(od[2:length(od)]/od[1:(length(od)-1)])/0.5
#this is still not the growth rate as we know it because
#they use log10
#we need to multiply the actual values by log(10)
mupaper<-mupaper*log(10)
#then they obtain the growth rate averaging this
#slope over the three time points centered
#on the time point where mu is maximum
w<-which(mupaper==max(mupaper,na.rm = T))
mu<-sum(mupaper[c(w-1,w,w+1)])/3

# chunk 4

#now let's do the estimation differently,
#using regression
#from the model
#log(x(t))=log(x(0))+mu t
#therefore, if we have log x(t) (the natural log of the optical density)
#at time t
#we can estimate mu through linear regression
#first we need to identify the interval
#where the growth is indeed exponential
lines(c(7.5,7.5),c(-10,10),col="blue")
lines(c(5,5),c(-10,10),col="blue")
#more or less in between 5 and 7.5
#this gives us 6 data points to estimate the slope
w<-which(tms<=7.5 & tms>=5)
#extract the data points
x<-tms[w]
#take natural log of the od
y<-log(od[w])
#build a model
mdl<-lm(y~x)
s<-summary(mdl)
s
#add line with slope mu
lines(tms,mdl$coefficients[1]+tms*mdl$coefficients[2],col="red",lwd=2)
mu_regression<-mdl$coefficients[2]
#s$coefficients[2,]
#let's see how far the two estimates are
#ny using the confidence interval of the 
#slope estimated through regression

abs(mu-mu_regression) / s$coefficients[2,2]
#
#what's the doubling time in minutes?
60*log(2)/mu_regression

