
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

def main(years: list[int], cities: list[str], daily_mean: int) -> None:
    print(f"Analyze PM2.5 data for {years} years")
    # merge data 
    dfs_clean = []
    dfs_exceed = []
    ## folder with data
    for year in years:
        input_dir = PROJECT_ROOT / "results" / "pm25" / str(year)
        clean_df = pd.read_csv(input_dir / 'clean_data.csv', parse_dates=[0], index_col=0)
        dfs_clean.append(clean_df)
        exceed_df = pd.read_csv(input_dir / 'daily_exceedances.csv')
        dfs_exceed.append(exceed_df)

    ## take intersection of common stations
    common_stations = list(
        reduce(set.intersection, (set(df.columns) for df in dfs_clean))
    )
    ## update dfs_clean
    dfs_clean = [df[common_stations] for df in dfs_clean]
    ## merge dfs
    combined_df = pd.concat(dfs_clean, axis=0).sort_index()
    ## drop `na values` it was done but to be sure
    combined_df = combined_df.dropna(how="all")

    ## pulled results 
    combined_df.index = pd.to_datetime(combined_df.index)
    combined_df = combined_df.sort_index()
    
    # analysis 
    ## Mean pM2.5 concentration 
    #TODO - create names for plots connected with cities 
    plot1_name = 'plot_years_trend_cities' # !!! change in snakefile
    years_trend_cities(combined_df, cities=cities, years=years, save_path=PLOTS_DIR / plot1_name)


    # create md file 


if __name__ == "__main__":
    # args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
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
    )