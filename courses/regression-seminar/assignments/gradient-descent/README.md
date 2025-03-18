## nomenclature
residual - in linear regression: real_point_value - estimated_point_value

## Tests

### functions 
- RSS (residaul sum of squares)
    - it is cost function which return error value

- gradient descent 
    - arguments
        - x: argument array
        - y: values array
        - cost function: function to optimilize
        - d_cost_function: derivative of cost function 
            - it is easier in usage
        - iterations: maximum number of iterations
        - learning_rate: scalar for derivate of function
        - stopping_threshold: minimum error we want to obtain: 
            - when we reach this error we stop iteration 

    - IMPORTANT
        to assure method converges we need to choose $\tau$ between $[0, 2/L]$ where $L$ is lipstchitz constant (addnotation to theorem) 