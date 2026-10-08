#read in grindR
remotes::install_git("https://bitbucket.org/stan_maree/grind.git")
library(Grind)

#first the model is defined
model <- function(t, state, parms) {
  with(as.list(c(state,parms)), {
    
    dA <- r*A*(1 - A/k) - c*A*Z/(s+A)
    dZ <- - q*Z + p*c*A*Z/(s+A)
    
    return(list(c(dA, dZ)))  
  }) 
}  

#then the parameter values are given
p <- c(r=4,k=50,c=10,s=10,q=0.75,p=0.1)  # p is a named vector of parameters

#and finally the begin state of the variables is given
s <- c(A=1,Z=1)                          # s is the state, the initial values of the variables

#run a simulation for tmax timesteps, generate an output datapoint every tstep
run(tmax=200, tstep=0.1)

#now first vary k and then each time make a new timeplot
#(e.g. increase k in steps of 5 from 20 to 100)
run(tmax=200, tstep=0.1,parms=c(r=4,k=20,c=10,s=10,q=0.75,p=0.1))

#make a phase plane: indicate max of x and y axis, and show the vectors as well
#again, vary k and then each time make a new nullcline plot
#think a bit about what you observe, and try to link the phase planes to the time plots
plane(xmax=120,ymax=15,vector=TRUE)
plane(xmax=120,ymax=15,vector=TRUE,parms=c(r=4,k=20,c=10,s=10,q=0.75,p=0.1))

#to plot time dynamics within the phase plane (i.e. trajectories):
plane(xmax=120,ymax=15,vector=TRUE)
run(tmax=200, tstep=0.1,traject=TRUE)

#go to equilibrium, and determine Jacobian, eigenvalues and stability; draw equilibrium position in phase plane
newton(jacobian=T,plot=T,state=c(A=0,Z=0))
newton(jacobian=T,plot=T,state=c(A=50,Z=0))
newton(jacobian=T,plot=T,state=c(A=30,Z=30))

