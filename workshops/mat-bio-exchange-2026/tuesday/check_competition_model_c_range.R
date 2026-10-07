library ( deSolve )
# define the system

#Time is the simulation time
#State at the first iteration is the initial condition
#then it is the abundance of the variables
#Pars is a list containing the parameters required by the model, in this case
#c and the growth rates of the two species in the system

#fx also is a parameter, but it is recalculated at each integration step
sist <- function( Time , State , Pars ){
  with ( as.list ( c ( State , Pars )) ,{
    x <- State
    fx <- mux * x^( c - 1 ) - muy*( 1-x )^( c - 1 )
    x <- x *( 1 -x )* fx
    list ( x )
  })
}
# initial conditions
xini <- matrix ( 0 , nrow = 1 , ncol = 1 )
#note that we start with x<.5
#below, x has the largest growth rate
xini [ 1 ,1 ] <- 0.45
# define simulation time
times <- seq (0, 100,.5)
# define parameters for the model and run the simulation
#fitness of x is higher
muy <- .65
mux <- .8
#define params, change only c
#we run a few simulations for each c situation (< or >1)
Pars <- list( mux = mux , muy = muy , c =.9 )
cless1_1 <- ode( xini , times , sist , Pars , method = "bdf" )
Pars <- list ( mux = mux , muy = muy , c =.85 )
cless1_2<- ode( xini , times , sist , Pars , method = "bdf" )
Pars <- list ( mux = mux , muy = muy , c =.5 )
cless1_3<- ode( xini , times , sist , Pars , method = "bdf" )

#c>1
Pars <- list ( mux = mux , muy = muy , c = 1.7 )
cmore1_1<- ode( xini , times , sist , Pars,method="bdf")
Pars <- list ( mux = mux , muy = muy , c = 2 )
cmore1_2<- ode( xini , times , sist , Pars , method = "bdf" )
Pars <- list ( mux = mux , muy = muy , c = 3)
cmore1_3<- ode( xini , times , sist , Pars , method = "bdf" )

# some simple plot to see what happens
#time evolution for the system when c<1
plot ( cless1_1[ , 1 ] , 
       cless1_1[ , 2 ] , 
       type = "l" , 
       ylim = c ( 0 , 1) , 
       col = "pink" ,
       lwd=2,main="Evolution in time of the system \n at different c values",
       xlab="Time",ylab="x_1")
lines( cless1_2[ , 1 ] , cless1_2[ , 2 ] , type = "l" , col = "red" ,lwd=2)
lines( cless1_3[ , 1 ] , cless1_3[ , 2 ] , type = "l" , col = "darkred" ,lwd=2)
#c>1
lines( cmore1_1[ , 1 ] , cmore1_1[ , 2 ] , type = "l" , col ="lightblue" ,lwd=2)
lines( cmore1_2[ , 1 ] , cmore1_2[ , 2 ] , type = "l" , col = "blue" ,lwd=2)
lines( cmore1_3[ , 1 ] , cmore1_3[ , 2 ] , type = "l" , col = "black" ,lwd=2)

legend(x=80,y=0.55,
       c("c=.9","c=.85","c=.5","c=1.7","c=2","c=3"),
       fill=c("pink","red","darkred","lightblue","blue","black"),
      cex=.8)

#the important qualitative change from c=2 to c=3
#can be explored graphically in more detail
#we will focus only on steady states
#generate a series of values for c around the change point
valC<-seq(1.75,2.2,0.01)
SS<-NULL
for(i in 1:length(valC)){
  Pars <- list ( mux = mux , muy = muy , c = valC[i])
  tmp<- ode( xini , times , sist , Pars , method = "bdf" )
  SS[i]<-tmp[length(tmp)]
}

plot(valC,SS,main="Change in behavior depending on c",ylab="x_1 at steady state",xlab="c")
#or we can do the same for the entire range

