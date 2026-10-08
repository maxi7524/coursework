#read in grindR
remotes::install_git("https://bitbucket.org/stan_maree/grind.git")
library(Grind)

#first the model is defined
model <- function(t, state, parms) {
  with(as.list(c(state,parms)), {
    
    du <- gamma*(a-u-rho*v*u/(1.+u+k*u^2))
    dv <- gamma*(alpha*(b-v)-rho*u*v/(1.+u+k*u^2))
    
    return(list(c(du, dv)))  
  }) 
}  

#then the parameter values are given
p <- c(gamma=25.,a=92.,b=64.,rho=18.5,k=0.1,alpha=1.5)  # p is a named vector of parameters

#and finally the begin state of the variables is given
s <- c(u=1,v=1)                          # s is the state, the initial values of the variables

#run a simulation for tmax timesteps, generate an output datapoint every tstep
run(tmax=0.5, tstep=0.005)

#make a phase plane: indicate max of x and y axis, and show the vectors as well
plane(xmax=100,ymax=50,vector=TRUE)

#now on a log-log plot, to make it easier to see how the nullclines go
plane(xmin=0.1,xmax=100,ymin=5,ymax=50,log="xy",vector=TRUE)

#go to equilibrium, and determine Jacobian, eigenvalues and stability; draw equilibrium position in phase plane
newton(jacobian=T,plot=T)
