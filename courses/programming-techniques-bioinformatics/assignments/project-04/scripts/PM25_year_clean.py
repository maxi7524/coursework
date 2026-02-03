
### -------------------- ###
###  libraries
### -------------------- ### 

# script functionality
import argparse
import yaml
import pandas as pd
from pathlib import Path


# functions from project 1 and 3  
from load_data import download_gios_archive, clean_gios_data2, clean_column_names
from analyse_data import map_old_to_new_codes, get_daily_exceedances

### -------------------- ###
###  Variables
### -------------------- ### 
# data addresses
gios_url_ids = {
    2015: "236", 
    2018: "603",
    2021: "486",
    2024: "582"
}
gios_pm25_file = {
    2015: "2015_PM25_1g.xlsx",
    2018: "2018_PM25_1g.xlsx",
    2021: "2021_PM25_1g.xlsx",
    2024: "2024_PM25_1g.xlsx"
}
# set path for script ()
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[0]

### -------------------- ###
###  main code 
### -------------------- ### 

def main(year: int, daily_mean: str) -> None:
    # variables
    ## creating dir for data
    output_dir = PROJECT_ROOT / "results" / "pm25" / str(year)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f'output dir: {output_dir}')
    
    # debug part 
    print(f"Running year for year: {year}")

    # clean files
    ## download data
    year_raw_df = download_gios_archive(
        year=year, 
        gios_id=gios_url_ids[year],
        filename=gios_pm25_file[year] 
    )

    ## clean data
    year_clean_df = clean_gios_data2(year_raw_df)
    year_clean_df = clean_column_names(year_clean_df)

    ## map old to new 
    year_clean_df.rename(columns=map_old_to_new_codes(), inplace=True)

    ## drop na values
    year_clean_df = year_clean_df.dropna(how="all")

    ## save clean files
    year_clean_df.to_csv(
        output_dir / f'clean_data.csv',
        index=True, 
        date_format="%Y-%m-%d %H:%M:%S"
    )
    
    # daily_exceedances
    ## get df
    year_exc, _ = get_daily_exceedances(year_clean_df, daily_mean)

    ## save daily_exceedances file
    year_exc.to_csv(
        output_dir / f"daily_exceedances.csv",
        index=True, 
        date_format="%Y-%m-%d %H:%M:%S"
    )

if __name__ == "__main__":
    # args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--config", type=str, required=True)
    args = parser.parse_args()

    # extract config values
    with open(args.config) as f:
        cfg = yaml.safe_load(f)
        daily_mean = cfg['daily_mean']


    main(
        year=args.year,
        daily_mean=daily_mean,
    )