Regresja liniowa
- charakterystyczne jest że mamy tutaj explicite podana funkcje do liczenia błędu bez potrzeby stosowana gradient descent 


### Linear regression 

#### introduction 

Problem (one dim): 
we want to predict:
$$y_i = \beta_0 + \beta_1 x_i$$
- we have linear equation of type:
    two variables many rows -> it will not have solution 
- solution will be aproximated -> we need to find measure of our approximation (cost function) 
- IMPORTANT:
    - we need to check linear independce between features, if two feature columns are depended our matrix will be singular 

cost function: RSS(Residual Sum of Squrares)
$$RSS  = \sum_{j=1}^n (\beta_0 + \beta_i x_j - y_j)^2$$
in matrix language
$$|| \beta \cdot 1 + \beta_1 \cdot X - Y||^2$$

problem to solve:
$$Y = X\beta$$
where $X = [1 | x_1 | \ldots | X_{p-1}$

so solution to our problem is
$$\beta = (X^TX)^{-1} X^Ty$$

conditions on $X^TX$ matrix: 
- invertible if $X$ is full rank
- TO KNOW: $XX^T$ do not need to be invertible

numerical problems 
- $rank(X) < 10^6$ - Gauss method 
- $rank(X) > 10^6$ - gradient descent method 
- $rank(X) > 10^8$ - stochastic gradient descent method

usage 
- always check missing data
- check colinearity of features


Normalization 
- motivation 
    - we need to calculate data 
- linear transposition 
    - because this is linear transpose it does not change properties of linear regression 
    - it helps numerically $\Leftarrow$ it reduces computation 
    - TODO: regularization (later) 

#### Statistics point of view

we describe problem as: 
$$y = X\beta \epsilon, \quad \epsion ~ \mathcal{N}(0, \sigma^2 I$$

Gausa-Markov theorem:
$$\hat{\beta} = (X^TX)^{-1}X^Ty$$ is unbiased estimator for $\beta$ with minimal variance amd highest likelihood (bayesian term ?) 

and more we have that 
$\hat{sigma}^2 = \frac{RSS}{n-p}$ ~ unbiased estimator of $\sigma^2$, where $n-p$ are degrees of freedom. 

Measuring score of our model:
$$R^2 = 1 - \frac{RSS}{TSS}$$

where $RSS$ is real estimation and RSS is theoretical 

$R^2$ measure the fraction of variation of $y$ how much is explained by the model.

why RSS
- properties 
    - having analytical solution 
    - statistical properites (unbiased, minimal variance etc) 
- other functional can by also used but in certain situations 

slide 15/16 (end of presentation )



#### Lecture about 

checking assumptions 
- we always need to check if data is colinear (with certain tests)
- also error values 

cross validation
- method is splitting our data on $cv$ amount, than performs test with 1 test group and other as learning group, 
- i do not understand why we want to perform this on models from task 1,2 it only depends on data?


