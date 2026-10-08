library(deSolve)
library(RColorBrewer)
library(pheatmap)
#here you can play with a relatively complicate quasi-species model
#to check the ability to explore efficiently the fitness landscape.
#in short we have:
#1. binary sequences of length 20
#2. they are grouped into 20 classes grouping sequences with the same number of 1s
#3. the 20 classes are grouped into 10 fitness groups depending on the number of 1s
#4. maximum fitness is for the master sequence and the other groups receive
#a decreasing fitness value with their distance from the master
#5. mutations are modeled in an explicit way, using a 20x20 mutation
#matrix derived from a certain error rate (the code of the model and the function for obtaining the 
#mutation matrix is in script model_and_Q_for_qs.R in this same folder)




#the model
source("model_and_Q_for_qs.R")

#------------------------------------------------------------
# Parameters
#------------------------------------------------------------
# sequence length
L <- 20   

#we define classes based on the number of ones 
#(sort of GC content for binary sequences)
#there can be from 0 to L ones in a sequence
classes <- 0:L
state_names <- paste0("x", classes)

#we define fitness values for all classes
#the master sequence will have the largest one
#if you want you can change these, keep 10 values and the maximum for the master
#an assumption is that the more 1s you have in the sequence the smaller the fitness
#but you are not obliged to respect this, in reality things are much more complicate!
#therefore you can try any scenario you want
fitness_values <- seq(
  from = 5,
  to = 1,
  length.out = 10
)

# Master = group 1
# Classes k = 1,...,20 are divided in 9 fitness groups
fitness_group <- integer(L + 1)
fitness_group[1] <- 1

for (k in 1:L) {
  fitness_group[k + 1] <- 2 + floor((k - 1) * 9 / L)
}

fitness <- fitness_values[fitness_group]
names(fitness) <- state_names

table(round(fitness,digits = 2))
#if only two fitness classes
# fitness <- rep(1, L + 1)
# fitness[1] <- 1.5
data.frame(
  Hamming_distance = 0:L,
  fitness_group = fitness_group,
  fitness = fitness
)

#define time step for the simulation output
#integration will be done in [0,500] then
#these time points will be output
times <- seq(
  from = 0,
  to = 500,
  by = 0.1
)

#vector to store initial abundances of the classes
initial_state <- rep(0, L + 1)

#here we use a population where the 
#master sequence IS NOT PRESENT, while
#there is a UNIFORM mix of all the other classes
present<-2:length(initial_state)

#initial_state[1] is the master sequence.
#another experiment can be done by setting
#initial_state[1]<-1
#and commenting out the next line
#in this way you will start from a population composed 
#of only the master sequence
initial_state[present] <- 1/20
names(initial_state) <- state_names

#define a range of mutation rates
#at each iteration in the next for loop,
#one value will be used to derive a mutation matrix to be fed into the model
mut_prob_per_site<-10^seq(from =-3, to=-.5, by=0.1)
#let's get one mutation matrix just as an example
tmp1<- make_mutation_matrix(L, mut_prob_per_site[1])
pheatmap(log10(tmp1),cluster_rows = F,cluster_cols = F)
#or
tmp2<- make_mutation_matrix(L, mut_prob_per_site[length(mut_prob_per_site)/2])
pheatmap(log10(tmp2),cluster_rows = F,cluster_cols = F)

#
CL<-(colorRampPalette(brewer.pal(9,"Spectral"))(length(mut_prob_per_site)))
#to store the steady state abundances
D<-matrix(0,nrow=length(mut_prob_per_site),ncol=length(fitness_values))

for(i in 1:length(mut_prob_per_site)){
  #we run the simulation many times, each time with a different mutation rate
  #therefore we need to recalculate the mutation matrix every time
    u <- mut_prob_per_site[i]   # mutation probability per site and replication
    Q <- make_mutation_matrix(L, u)
    
    # Probability of perfect replication of the master
    #Q[1, 1]
    
    # Expected value: (1-u)^L
    #(1 - u)^L
    
    #store the parameters in a list
    parameters <- list(
      L = L,
      Q = Q,
      fitness = fitness
    )
    
    #run the simulation with this set of parameters
    simulation <- ode(
      y = initial_state,
      times = times,
      func = quasispecies_model,
      parms = parameters,
      method = "lsoda",
      rtol = 1e-10,
      atol = 1e-12
    )
    
    simulation <- as.data.frame(simulation)
    simulation$mutants <- 1 - simulation$x0
    #just to get median of the abundance of classes belonging to the same fitness group
    bxpl<-boxplot(unlist(simulation[nrow(simulation),2:22])~
                    as.factor(fitness_group),plot=F)
    #store them
    #we are not storing the actual abundance of the classes
    #but the total average abundance of the fitness groups
    D[i,]<-bxpl$stats[3,]
    if(i==1){
      plot(fitness_values,bxpl$stats[3,],type="l",col=CL[i],lwd=2,ylab="x",xlab="Fitness")
    }else{
      lines(fitness_values,bxpl$stats[3,],type="l",col=CL[i],lwd=2)
    }
    }


rownames(D)<-round(mut_prob_per_site*10000)/10000
colnames(D)<-round(fitness_values*10)/10
pheatmap(log10(.01+D),cluster_rows = F,cluster_cols = F,col=rev(CL))
