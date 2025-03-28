Ridge regression
- it is regression which takes adjustment in $L$ norm

## exercise 

cross validation: (validation rename)

- $lambda$ meta parameter 
- we need to find best hyper-parameters ?
- strategy
    - data consuming 
        - we split data 60%, 20%, 20%
        - on 60% we train model for different parameters 
        - on 20% we choosing best model (we make )
        - on last 20% we are checking characteristics of models 




## my notes 

transformers 
- it is special type of objects which contain, fit transform features, so we can automate process by doing one pipeline 

[//]: # TODO we need to look about difference in these objects
Predictor 
- object that have method predicting values (learning) 


pipelines 
- it takes as arguments *transformers and 
- generally we have object Pipeline, which manage this but it need to informed about type object, in use we should use make_pipeline function which do it automatically for ous 