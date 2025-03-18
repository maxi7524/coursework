### Logistic Regression 

name 
- regression - it predicts probability value 
- logistics - it is about probability and logistics indicates categorical data (we have finite amount of objects)

adjustment 
- cost function (cross entropy) 
    we need to create cost function which give ous extreme values for single points
    we do it using transformation from $\mathbb{R} \rightarrow (0, 1)$ 
- overfitting, underfitting
    is the same ous in linear regression 
    TODO ~ slide with construction 

- logarithm usage
    better scale for calculating, (numerically)
    to maximize answer difference (?)

derivation 
- prediction of probability of $y_i$
    TODO ~ slajd 

Interpretation of cost function
- we creating this in fashion of LE, and latter we want to minimize $-J(B)$ so we are finding MLE. 
- $\beta$ parameter sharpens the step (TODO try this out)

TODO exercise
- how to separate data using line ??? 
- this ellipse from lecture when we have data separated in circle not in line 
(transport to higher dimensions)
$(x, y) -> (x, y, x^2 + y^2)$ and we optimize third one 

TODO 
- stratify method in train test split ~ for equally splitting classes for training !!!!
- learn how this works, how interpret this 
- do some basics calculations and get intuition behind this
### Description of model 
characteristics 
- sensitivity(recall) - what fraction of true positive examples are captured 
- specitifiy
- precision 
programming (methods with crossing values, and how fast interpret this)

to calculactions 
$F_1$ - harmonic mean of sensitivity and precision (they are opposite in sense (?)) 
