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
- app
    - *main.py*: FastAPI server code
- models: Trained model files
    - *lr_model.pkl*
    - *pls.pkl*
    - *poly_model.pkl*
    - *pt_transform.pkl*
    - *scaler.pkl*
- main.ipynb: This file contains the whole code (except for FastAPI code)

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
    - box-cox transformation and log transformation
    - PCR (0.95 explainability -> 8 components) and PLS (8 components)
- Splitting Data

### Part 3 - model training 
Takes X_train, X_test, Y_train, y_yest, makes predictions using regression models, and evaluates them
- Train models
    - Linear regression
    - Polynomial regression with ridge regularization
- Model evaluation
    - MSE
    - R²
    - Pearson correlation coefficient
    - Predicted vs. observed plot

### Part 4 - model sharing
Enables using trained models in FastAPI
- Endpoint `/predict-energy`
    - accepts input data in JSON format
    - returns energy values predicted by both models

## Problem
The aim of the project is to predict the average daily energy consumption of a single-family home in Sceaux (France) based on historical data on energy consumption and weather conditions.

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
- Part 3 - training regression models
- Part 4 - model sharing