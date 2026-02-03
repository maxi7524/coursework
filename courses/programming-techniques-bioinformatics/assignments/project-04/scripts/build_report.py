
### -------------------- ###
###  libraries
### -------------------- ### 

# script functionality
import argparse
import yaml
import pandas as pd
from pathlib import Path
import os 

from functools import reduce


# functions from project 1 and 3  
from analyse_data import years_trend_cities

### -------------------- ###
###  Variables
### -------------------- ### 

# set path for script ()
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[0]
DATA_DIR = PROJECT_ROOT / 'results' / 'pm25'
PLOTS_DIR =  PROJECT_ROOT / "results" / "report_files" 
LITERATURE_DIR = PROJECT_ROOT / "results" / "literature"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

### -------------------- ###
###  main code 
### -------------------- ### 

def main(years: list[int], cities: list[str], daily_mean: int, output) -> None:
    # variables management

    out = Path(output)
    # document write
    with open(out, "w") as f:
        # tytuł 
        f.write('# Raport Task 4\n\n')

        # text (divided for years)
        for year in years:
            # header
            f.write(f"### Wyniki rok {year} \n\n")        

            # table 
            df = pd.read_csv(DATA_DIR / str(year) / 'daily_exceedances.csv')
            f.write(df.head().to_markdown(index=False))
            # spacing
            f.write("\n\n")

        # image
        plot_1_path = 'report_files/plot_years_trend_cities.png'
        f.write(f"![PM2.5 years trend]({plot_1_path})\n\n")


if __name__ == "__main__":
    # args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    # extract config values
    with open(args.config) as f:
        cfg = yaml.safe_load(f)

        # analysis config
        years = cfg['years']
        cities = cfg['cities']
        daily_mean = cfg['daily_mean']


    main(
        years=years,
        cities=cities,
        daily_mean=daily_mean,
        output = args.output
    )