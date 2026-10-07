#read in grindR
remotes::install_git("https://bitbucket.org/stan_maree/grind.git")
library(Grind)

#first the model is defined
#dS/dt captures the sheep dynamics, note that we just type dS
#dW/dt captures the wolf dynamics, note that we just type dW

model <- function(t, state, parms) {
  with(as.list(c(state,parms)), {

    #this model describes wolves (W) eating sheep (S)   
    dS <- b*S-ds*S-p*W*S
    dW <- c*p*W*S-dw*W
    
#make sure to return all temporal derivatives      
    return(list(c(dS,dW)))  
  }) 
}

#then the parameter values are given
#"b" is the birth rate of sheep, for example 1.5/year (i.e. 3 lambs per ewe per year)
#"ds" is the natural death rate of sheep, for example 0.14/year (in the wild, sheep can 
# become around 7 years old)
#"p" is the capturing rate of sheep by wolves. This parameter very much depends on the terrain
# and the exact units in which the variables are expressed (number of sheep or
# concentration of sheep per what kind of area). Here we put it to 1 per wolf per year.
#"c" is the amount of wolf offspring per captured sheep. If sheep and wolves are 
# expressed in biomass, the value is expected to be close to 0.1 wolf per sheep,
# using a typical 10% conversion efficiency when moving up one trophic level. 
# If the variables are instead expressed in number or density of sheep and wolves, 
# we also have to take the typical weight of wolves and sheep into account. While
# wolves weigh around 35 kg, sheep weigh around 70 kg. When thinking in numbers or density,
# the value of c should therefore rather be 0.2 wolf/sheep
#"dw" is the natural death rate of wolves. in the wild, wolves become around 8 year old, 
# a reasonable value for dw is thus 0.125/year.

p <- c(b=1.5,ds=0.14,p=1,c=0.2,dw=0.125) # p is a named vector of parameters

#and finally the initial conditions (begin state) of the variables is given
s <- c(S=1,W=1) # s is the state, the initial values of the variables

#run a simulation for tmax timesteps, generate an output datapoint every tstep
#run the model for 100 years
run(tmax=100, tstep=0.1)
#run the model for 100 years
run(tmax=100, tstep=0.1,xlab="Time [years]",ylab="Population size",)

#start with no sheep
s <- c(S=0,W=1)
#run the model again
run(tmax=100, tstep=0.1)
#without any food, the wolves present an exponential decay
run(tmax=100,tstep=0.1,show=c("W"),ymin=1e-5,log="y",xlab="Time [years]",ylab="Wolf population")

#the most relevant arguments of run() that you might want to change one day, and their default values
run(tmax=100, tstep=1, state=s, parms=p, odes=model, ymin=0, ymax=NULL,
  log="", xlab="Time", ylab="Density", tmin=0, draw=lines,
  show=NULL, timeplot=TRUE, traject=FALSE,
  table=FALSE, add=FALSE, legend=TRUE, solution=FALSE, lwd=2)

#make a phase plane: indicate min and max of x and y axis, and show the vectors as well
plane(xmax=5,ymax=5,vector=TRUE)
#show trajectory in phase plane
s <- c(S=1,W=1)
run(tmax=100, tstep=0.1,traject = TRUE)

#the most relevant arguments of run() that you might want to change one day, and their default values
plane(xmin=-0.001, xmax=1.05, ymin=-0.001, ymax=1.05, 
      xlab="", ylab="", log="", npixels=500, 
      state=s, parms=p, odes=model, x=1, y=2, 
      time=0, grid=5, show=NULL, addone=FALSE, 
      portrait=FALSE, vector=FALSE, add=FALSE, 
      legend=TRUE, zero=TRUE, lwd=2, col="black", pch=20)
