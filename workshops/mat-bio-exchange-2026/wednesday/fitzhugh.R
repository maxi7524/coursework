#read in grindR
remotes::install_git("https://bitbucket.org/stan_maree/grind.git")
library(Grind)

#first the model is defined
model <- function(t, state, parms) {
  with(as.list(c(state,parms)), {
    
    dV <- -V*(V-a)*(V-1)-W
    dW <- eps*(V-b*W)
    
    return(list(c(dV, dW)))  
  }) 
}  

#then the parameter values are given
p <- c(a=0.05,eps=5e-3,b=3)  # p is a named vector of parameters

#and finally the begin state of the variables is given
s <- c(V=0,W=0)                          # s is the state, the initial values of the variables

#run a simulation for tmax timesteps, generate an output datapoint every tstep, y-axis from 0 to 1
run(tmax=1000, tstep=1.,ymin=-0.5,ymax=1)

#run for different starting points
run(tmax=1000, tstep=1.,ymin=-0.5,ymax=1,state=c(V=0.01,W=0))

#make a phase plane: indicate min and max of x and y axis, and show the vectors as well
plane(xmin=-.5,xmax=1.25,ymin=-0.05,ymax=0.20,vector=TRUE)

#go to equilibrium, and determine Jacobian, eigenvalues and stability; draw equilibrium position in phase plane
newton(jacobian=T,plot=T)

#run a simulation and display it in the phase plane
run(tmax=1000, tstep=1.,traject = T)
#run a simulation for different initial point and display it in the phase plane
run(tmax=1000, tstep=1.,state=c(V=0.01,W=0),traject = T)

