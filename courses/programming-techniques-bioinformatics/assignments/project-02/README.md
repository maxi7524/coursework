# Introduction

# repository structure
- data
    - *raw_EP.pkl*
        - size: 192M
    - *raw_METEO.pkl*
        - size: 2.8K
    - *raw_combined.json*
        - size: 27M 
        - outer joined *raw_EP* and *raw_METEO.pkl*
- main
    This file contains whole code

# main
## Structure
### Part 1 - download data
- Download data from sites
- Load data and create YYYY-MM-DDTHH:mm:ss±hh:mm data format (to hh resolution)
- Join datasets and save them to `raw_combined.json`
### Part 2 - data engineering 
Takes raw data, return clean data in X_train, X_test, Y_train, y_yest
- Clean data
- Feature engineering 
- Splitting Data
### Part 3 - model training 
Takes X_train, X_test, Y_train, y_yest ... have fun :) 

### Part 4 - model sharing  


## Problem

## Data
[raw_EP.pkl](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption) contains:
- 'data': contains data for task
- 'metadata': contains metadata 
    - `num_instances`: amount of instances (leak check)
    - `additional_info`: information about data 
    - `variable info`:  information about data format
- 'variables': contains information about variables (type, missing values)
[raw_METEO.pkl](https://open-meteo.com/)
- contains data with weather features
    - `temperature`
    - `winds`
    - agriculture 

## Solutions



# Contribution
## Max Stróżyk
- Documentation
- Part 1 - download data
- Part 2 - data engineering 
## Anna Szymik