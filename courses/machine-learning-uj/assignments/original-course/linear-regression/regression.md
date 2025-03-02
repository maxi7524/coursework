# Basic ideas 

## EIV - measurment eror model 


## Linear methods for regression 

### Assumptions 
- $E[Y|X]$ is linear on $X_i, \ldots, X_p$ (amount of parameters)
### Usage
- simple models which works with small amount of probes 
- main usage is from data transformation 
### variance calculations
- least square methods
- better is orthogonal least square method for calcualting error (it get rid of error related to measurments error) - proofs for best approximation given some assumptions
### construcion 
$$X \in M_{N \times (p+1)}$$

We need to minimize the least squre problem:

$$RSS(\beta) = (y - X\beta)^T(y-X\beta)$$

Be calculating minimum value for $\beta$ we are find that solution is (find from book) 

$$$$