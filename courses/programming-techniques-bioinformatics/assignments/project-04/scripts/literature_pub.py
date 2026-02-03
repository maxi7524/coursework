
### -------------------- ###
###  libraries
### -------------------- ### 

# script functionality
import argparse
import yaml
import pandas as pd
from pathlib import Path

from functools import reduce


# functions from project 1 and 3  
from analyse_data import years_trend_cities

### -------------------- ###
###  Variables
### -------------------- ### 

# set path for script ()
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[0]
PLOTS_DIR =  PROJECT_ROOT / "results" / "report_files" 
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

### -------------------- ###
###  main code 
### -------------------- ### 

def main(entrez_mail: str, query: str, retmax: 200) -> None:
    
    # 

    entrez_mail=entrez_mail,
        query=query,
        retmax=retmax,
    
    
    pass


if __name__ == "__main__":
    # args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    args = parser.parse_args()

    # extract config values
    with open(args.config) as f:
        cfg = yaml.safe_load(f)

        # analysis config
        entrez_mail = cfg['entrez_email']
        query = cfg['pubmed']['query']
        retmax = cfg['pubmed']['retmax']


    main(
        entrez_mail=entrez_mail,
        query=query,
        retmax=retmax,
    )