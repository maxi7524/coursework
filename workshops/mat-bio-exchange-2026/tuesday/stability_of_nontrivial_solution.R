library(Deriv)

#our model
fx <- function(x,c,a,b){
  x*(1-x)*(a* (x^(c-1))-b*((1-x)^(c-1)))
}


#we can use Deriv function to get the second derivative analytically
dfx<-Deriv(~fx(x,c,a,b),"x")

#which is the same formula I am writing below in function ddfx
ddfx<-function(x,c,a,b){
  e1 <- 1 - x
  e2 <- c - 1
  e3 <- c - 2
  (1 - 2 * x) * (a * x^e2 - b * e1^e2) + x * e1 * (a * x^e3 + b * e1^e3) * e2
  
}


#non trivial solution
#a and b are the two growth rates mu1 and mu2 in the slides,
#c has the same meaning
xstar<-function(a,b,c){
  1/(1 + (a/b)^(1/(c-1)))
}

a=1.5
b=2
#generate x levels in between 0 and 1
#HOWEVER
#consider that the stability analysis is only valid
#for the steady states

#here we have a singularity when c<1 at 0 and 1

xx<-seq(from=0,to=1,by=0.001)
par(mfrow=c(2,1))
C=3
plot(xx,ddfx(x=xx,c=C,a=a,b=b),
     type="l",
     col="blue",
     lwd=2,
     main="Super-exponential (C=2)",
     ylab = "d(system)@ x",
     xlab="x",
     xlim=c(xx[1]-.1,xx[length(xx)+.1]),
     ylim=c(-2,1))

lines(c(xstar(c=C,a=a,b=b),xstar(c=C,a=a,b=b)),c(ddfx(x=xstar(c=C,a=a,b=b),c=C,a=a,b=b),ddfx(x=xstar(c=C,a=a,b=b),c=C,a=a,b=b)),
      col="red",
      lwd=3,
      type="p",
      pch=18,cex=1.5)
lines(c(0,0),c(ddfx(x=0,c=C,a=a,b=b),ddfx(x=0,c=C,a=a,b=b)),
      col="darkgreen",
      lwd=3,
      type="p",
      pch=18,cex=1.5)
lines(c(1,1),c(ddfx(x=1,c=C,a=a,b=b),ddfx(x=1,c=C,a=a,b=b)),
      col="darkgreen",
      lwd=3,
      type="p",
      pch=18,cex=1.5)
abline(h=0,col="red")
C=.4
plot(xx,ddfx(x=xx,c=C,a=a,b=b),
     type="l",
     col="blue",
     lwd=2,
     main="Sub-exponential (C=0.4)",
     ylab = "d(system)@ x",
     xlab="x")

lines(c(xstar(c=C,a=a,b=b),xstar(c=C,a=a,b=b)),c(ddfx(x=xstar(c=C,a=a,b=b),c=C,a=a,b=b),ddfx(x=xstar(c=C,a=a,b=b),c=C,a=a,b=b)),
      col="darkgreen",
      lwd=3,
      type="p",
      pch=18,cex=1.5)
lines(c(0,0),c(ddfx(x=0.001,c=C,a=a,b=b),ddfx(x=0,c=C,a=a,b=b)),
      col="red",
      lwd=3,
      type="p",
      pch=18,cex=1.5)
lines(c(1,1),c(ddfx(x=.999,c=C,a=a,b=b),ddfx(x=1,c=C,a=a,b=b)),
      col="red",
      lwd=3,
      type="p",
      pch=18,cex=1.5)
abline(h=0,col="red")
#grid(col="black",lty=1)

