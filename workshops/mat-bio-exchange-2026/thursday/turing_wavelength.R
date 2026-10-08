#read in grindR
remotes::install_git("https://bitbucket.org/stan_maree/grind.git")
library(Grind)

#copy of newton function to get as output jac instead of eq;
#this is to check if we are actually potentially expecting a Turing pattern 
#in the first place
newtonjac <- function(state=s, parms=p, odes=model, time=0, positive=FALSE, jacobian=FALSE, vector=FALSE, plot=FALSE, silent=FALSE, addone=FALSE, ...) {
  # find a steady state
  # if (!is.numeric(x)) x <- index(x,names(state))
  # if (!is.numeric(y)) y <- index(y,names(state))
  One <- ifelse(addone, 1, 0)
  q <- rootSolve::steady(y=state,func=odes,parms=parms,time=time,positive=positive, ...)
  if (attr(q,"steady")) {
    equ <- q$y
    equ <- ifelse(abs(equ) < 1e-8, 0, equ)
    jac <- rootSolve::jacobian.full(y=equ,func=odes,parms=parms)
    eig <- eigen(jac)
    dom <- max(Re(eig$values))
    if (!silent) {
      print(equ)
      if (length(equ) == 2) {
        if (is.complex(eig$values[1])) {
          cat(ifelse(dom < 0, "Stable spiral point, ", "Unstable spiral point, "))
        } else if(prod(eig$values) > 0) {
          cat(ifelse(dom < 0, "Stable node, ", "Unstable node, "))
        } else cat("Saddle point (unstable), ")
      } else {
        cat(ifelse(dom < 0, "Stable point, ", "Unstable point, "))
      }
      cat("eigenvalues:\n")
      print(eig$values)
    }
    if (vector) {cat("Eigenvectors:\n"); print(eig$vectors)}
    if (jacobian) {cat("Jacobian:\n"); print(jac)}
    if (plot)
      points(equ[grind.env$x_plane] + One, equ[grind.env$y_plane] + One, pch = ifelse(dom < 0, 19, 1))
    if (silent) return(list(state=equ,jacobian=jac,values=eig$values,vectors=eig$vectors))
    return(jac)
  }
  cat("No convergence: start closer to a steady state")
  return(invisible(NULL))
}

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
eq<-newton(jacobian=T,vector=T,plot=T)

#we now want the Jac as output, to check if it still has the right structure
jac<-newtonjac(state=eq)

#give the diffusion rate of activator and inhibitor
Da<-1
Di<-40
#calculate wavelength
wavelength<-2*pi/sqrt((Da*jac[4]+Di*jac[1])/(2.*Da*Di))
wavelength
#field size, see "Largest size" under "Domain" after clicking tool symbol
largestside <- 20
wavenumber <- largestside/wavelength
wavenumber
