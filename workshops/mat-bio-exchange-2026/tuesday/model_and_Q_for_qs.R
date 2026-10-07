quasispecies_model <- function(t, state, parameters) {
  #mutation matrix
  Q       <- parameters$Q
  #fitness
  fitness <- parameters$fitness
  #length of sequences
  L       <- parameters$L
  
  # Reproductive contribution of each parental class
  reproduction <- fitness * state
  
  # Mean fitness
  phi <- sum(reproduction)
  
  # Mutation-selection dynamics
  dx <- as.vector(Q %*% reproduction) - phi * state
  
  names(dx) <- names(state)
  
  # Additional variables saved in the output
  mean_distance <- sum((0:L) * state)
  total_frequency <- sum(state)
  
  return(
    list(
      dx,
      phi = phi,
      mean_distance = mean_distance,
      total_frequency = total_frequency
    )
  )
}



#------------------------------------------------------------
# 2. Mutation matrix Q
#
# Q[i + 1, j + 1] =
# probability that a parent in class j generates
# an offspring in class i
#------------------------------------------------------------

make_mutation_matrix <- function(L, u) {
  
  Q <- matrix(
    0,
    nrow = L + 1,
    ncol = L + 1,
    dimnames = list(
      offspring = paste0("k", 0:L),
      parent    = paste0("k", 0:L)
    )
  )
  
  for (j in 0:L) {
    
    for (i in 0:L) {
      
      # a = number of 1 -> 0 mutations
      a_min <- max(0, j - i)
      a_max <- min(j, L - i)
      
      if (a_min <= a_max) {
        
        a <- a_min:a_max
        
        # Number of 0 -> 1 mutations
        b <- i - j + a
        
        # Total number of mutated sites
        n_mut <- a + b
        
        Q[i + 1, j + 1] <- sum(
          choose(j, a) *
            choose(L - j, b) *
            u^n_mut *
            (1 - u)^(L - n_mut)
        )
      }
    }
  }
  
  return(Q)
}



#alternative Q with only single point mutations allowed
make_Q_one_mutation <- function(L, u, normalize = TRUE) {
  
  Q <- matrix(
    0,
    nrow = L + 1,
    ncol = L + 1,
    dimnames = list(
      offspring = paste0("k", 0:L),
      parent = paste0("k", 0:L)
    )
  )
  
  p0 <- (1 - u)^L
  p1 <- u * (1 - u)^(L - 1)
  
  for (j in 0:L) {
    
    # No mutation
    Q[j + 1, j + 1] <- p0
    
    # 0 -> 1: movement away from the master
    if (j < L) {
      Q[j + 2, j + 1] <- (L - j) * p1
    }
    
    # 1 -> 0: backmutation towards the master
    if (j > 0) {
      Q[j, j + 1] <- j * p1
    }
  }
  
  if (normalize) {
    Q <- sweep(
      Q,
      MARGIN = 2,
      STATS = colSums(Q),
      FUN = "/"
    )
  }
  
  return(Q)
}



