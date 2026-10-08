#read in grindR
remotes::install_git("https://bitbucket.org/stan_maree/grind.git")
library(Grind)

#first the model is defined
#dA/dt captures the amount of allolactose
#dM/dt captures the amount of mRNA
#R is the level of repressor
#NOTE that R should be defined before it is being used

model <- function(t, state, parms) {
  with(as.list(c(state,parms)), {
  
  R = 1/(1+A^n)               # Repressor
  dA = M*L - delta*A - v*M*A/(h+A)  # Allolactose
  dM = c0 + c*(1-R) - d*M     # mRNA

  return(list(c(dA, dM)))  
  }) 
}

#then the parameter values are given
p <- c(L=1,c=1,c0=0.05,d=1,delta=0.2,n=5,v=1,h=2)
#and finally the initial state of the variables is given;
#NOTE that the sequence of the variables "(A=0,M=0)" should be the same
#as the return list of the model "return(list(c(dA, dM)))", as this links A to dA; M to dM
s <- c(A=0,M=0)

#run a simulation for tmax timesteps, generate an output datapoint every tstep
run(tmax=40, tstep=0.1)
#different starting point, different outcome
run(tmax=40, tstep=0.1,state=c(A=0.9,M=0))

#plot the phase plane
plane(xmax=4,ymax=1.2,vector=TRUE)

#find the equilibria
#use the command newton to go to the equilibrium nearest to the indicated starting point
#store the equilibrium levels of the variables
#plot=T shows the found equilibria in the phase plane; open circle is unstable, closed is stable
low <- newton(s,plot=T)
middle <- newton(c(A=0.8,M=0.2),plot=T)
high <- newton(c(A=2,M=1),plot=T)

# The saddle

#The unstable steady state in the middle is a saddle point. One can depict the stable and unstable direction in the saddle by plotting the two eigenvectors.
#The first and the second eigenvalue define the stable and unstable direction (manifold) respectively.
#Calling newton() with the option `silent=TRUE` returns a list containing the state, the eigenvalues and the eigenvectors. So we can do the following:
middle <- newton(c(A=0.8,M=0.2),silent=TRUE)
vec1 <- middle$vectors[,1]
vec2 <- middle$vectors[,2]
x <- middle$state[1]; y <- middle$state[2]
plane(xmax=4,ymax=1.2,vector=TRUE)

#the stable direction (eigenvector 1) is plotted in green and the unstable direction (eigenvector 2) in orange.
arrows(x+0.2*vec1[1],y+0.2*vec1[2],x,y,col="darkgreen",length=0.1)
arrows(x-0.2*vec1[1],y-0.2*vec1[2],x,y,col="darkgreen",length=0.1)
arrows(x,y,x+0.2*vec2[1],y+0.2*vec2[2],col="darkorange",length=0.1)
arrows(x,y,x-0.2*vec2[1],y-0.2*vec2[2],col="darkorange",length=0.1)

# Separatrix

#The saddle point spans up a separatrix defining the boundary between the basins of attraction of the two stable points.
#One can draw a separatrix by integrating backwards along the eigenvector pointing in the stable direction.
#We do so by starting a small step from the equilibrium into the stable direction, and then we run the model backwards:  
#lwd determines the line width; col the color (3=green); and pch="." hides the big bullet at the start of the trajectory
#NOTE, both tmax and tstep have to be negative in order to run a simulation backwards!
plane(xmax=4,ymax=1.2,vector=TRUE)
s <- middle$state + 0.01*vec1
run(tmax=-40,tstep=-0.01,traject=TRUE,lwd=3,col=3,pch=".")
s <- middle$state - 0.01*vec1
run(tmax=-40,tstep=-0.01,traject=TRUE,lwd=3,col=3,pch=".")

#bifurcation plot

#plot the equilibrium level of M for different values of deltav
#to do so, we plot the parameter on the x-axis and the variable on the y-axis
#this can be done with the function 'continue'.
#high: start on the equilibrium named 'high'
#x="L": indicate which parameter goes on the x-axis
#y="M": indicate which variable goes on the y-axis
#xmin=0,xmax=1: min and max value to be used for the parameter
#ymin=0,ymax=4: min and max value of the y-axis; break off the analysis when reaching those values
#add=T: don't throw away the previous lines, add the curves as additional curves
#NOTE that here three times the same line is drawn, as the line "folds back"
#but this is not generally the case
#NOTE that a thick red line indicates a stable equilibrium, a thin blue line an unstable one
#more general, unstable equilibria are indicated by dashed lines
continue(low,x="L",y="M",xmin=0,xmax=2,ymin=0,ymax=1.2)
continue(middle,x="L",y="M",xmin=0,xmax=2,ymin=0,ymax=1.2,add=T)
continue(high,x="L",y="M",xmin=0,xmax=2,ymin=0,ymax=1.2,add=T)

