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


## construction
- we create function which is standard algorithm, 
- we create decorator which stores values of index, error, time (between steps), steps parameters (depends on algorithm) 
- we will do certain amount of these runes so we will get ultiply dataframes and we can take mean with certain significance, 
- later whe n we have all of these we will do tests so we do not re run everything again when our methodology will change, add it later to readme summarized (about process) 


## tests
main question
- we ask how big matrix every algorithm can handle and how close we can get 
- we will test it 2/3 differetn costs function / one will be ellipses center around some point with very little slope so we can test how snesible algorithm is, (it it should jump through it if step size is bigger) 

testss
- amount of iteartion needed for constatnt error due to matrix size 
- taking time need for it to test if there is not system issiues because everyiteration should take approximataely same time (maybe in summary we will get different value d)
- add longer bits 128 for erro



do statystyki ~ jaki test do jakich danych należy stosować 

test statystyka 
- test chi^2 do przeliczneia 