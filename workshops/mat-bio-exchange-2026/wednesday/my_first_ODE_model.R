#read in grindR
remotes::install_git("https://bitbucket.org/stan_maree/grind.git")
library(Grind)

#first the model is defined
#dX/dt captures the population dynamics, note that we just type dX

model <- function(t, state, parms) {
  with(as.list(c(state,parms)), {

    #this model describes so-called logistic growth of the world population    
    dX <- r*X*(1-X/K)
    
    return(list(c(dX)))  
  }) 
}

#then the parameter values are given
#"r" is approximately the yearly growth rate of 0.024
#"K" is the carrying capacity of the earth, 10 billion people
p <- c(r=0.024,K=1e10) # p is a named vector of parameters

#and finally the initial conditions (begin state) of the variables is given
#the population size in 1950, 2.5 billion people
s <- c(X=2.5e9) # s is the state, the initial values of the variables

#run a simulation for tmax timesteps, generate an output datapoint every tstep
#run the model from 1950 untill 2100
run(tmax=150, tstep=1)
#run the model from 1950 untill 2100
run(tmax=150, tstep=1,xlab="Time [years since 1950]",ylab="World population",)

#start with no individuals
s <- c(X=0)
#run the model again
run(tmax=150, tstep=1)

#start the model again with the world population size in 1500
s <- c(X=425e6) # s is the state, the initial values of the variables
#run a simulation,minimum of y-axis is 100 million,only show X and use a log plot for the y axis
#note that this is very badly fitting the data
run(tmax=600,tstep=0.1,ymin=1e8,show=c("X"), log="y",xlab="Time [years since 1500]",ylab="World population")

#the most relevant arguments of run() that you might want to change one day, and their default values
run(tmax=100, tstep=1, state=s, parms=p, odes=model, ymin=0, ymax=NULL,
  log="", xlab="Time", ylab="Density", tmin=0, draw=lines,
  show=NULL, timeplot=TRUE, traject=FALSE,
  table=FALSE, add=FALSE, legend=TRUE, solution=FALSE, lwd=2)

