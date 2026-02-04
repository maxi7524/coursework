
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
from .analyse_data import years_trend_cities

### -------------------- ###
###  Variables
### -------------------- ### 

# set path for script ()
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[0]
DATA_PM25_DIR = PROJECT_ROOT / 'results' / 'pm25'
REPORT_DIR =  PROJECT_ROOT / "results" / "report_files" 
LITERATURE_DIR = PROJECT_ROOT / "results" / "literature"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

### -------------------- ###
###  main code 
### -------------------- ### 

def main(years: list[int], cities: list[str], daily_mean: int, output) -> None:
    print("Mergin results into report ...")
    # variables management

    out = Path(output)
    # document write
    with open(out, "w") as f:
        # title 
        f.write('# Raport Analizy Zanieczyszczenia PM2.5 i Publikacji Naukowych\n\n')
        f.write('Poniższy raport zawiera analizę stężeń PM2.5 w Polsce oraz przegląd publikacji naukowych poświęconych zagadnieniom zanieczyszczenia powietrza.\n\n')

        ### -------------------- ###
        ###  results part 
        ### -------------------- ### 
        f.write("## Wyniki Analiz \n\n")
        
        # Per year results  
        for year in years:
            # year header 
            f.write(f"### Rok {year} \n\n")        
            
            f.write(f"#### Analiza Stężeń PM2.5 \n\n")
            f.write(f"Tabela poniżej przedstawia 5 stacji pomiarowych z największą liczbą przekroczeń dziennych normą PM2.5 (wartość {daily_mean} µg/m³) w roku {year}:\n\n")
            ## pm25 part
            ### table 
            df = pd.read_csv(DATA_PM25_DIR / str(year) / 'daily_exceedances.csv')
            #### Write it to markdown
            f.write(df.head().to_markdown(index=False))
            f.write("\n\n")
            
            ## literature part
            f.write("#### Analiza Publikacji Naukowych \n\n")
            f.write("Poniżej znajduje się podsumowanie publikacji naukowych dotyczących zanieczyszczenia powietrza.\n\n")

            ### Tables
            #### Publications per year
            f.write("**Liczba publikacji w wybranych latach:**\n\n")
            df = pd.read_csv(REPORT_DIR / 'publications_per_year.csv')
            f.write(df.to_markdown(index=False))
            f.write("\n\n")

            #### top journals 
            f.write("**10 głównych czasopism publikujących artykuły na temat zanieczyszczenia powietrza:**\n\n")
            df = pd.read_csv(REPORT_DIR / 'top_journals_global.csv')
            f.write(df.to_markdown(index=False))
            f.write("\n\n")

          

        # ALl years 
        f.write("## Analizy Łączne \n\n")

        ## Pm 2.5
        ### Plot: plot_years_trend_cities
        f.write("### Trend Stężeń PM2.5 w Wybranych Miastach \n\n")
        f.write("Poniższy wykres pokazuje zmianę stężeń PM2.5 w poszczególnych miastach w latach 2014-2024:\n\n")
        plot_plot_years_trend_cities_path = 'report_files/plot_years_trend_cities.png'
        f.write(f"![PM2.5 trend w miastach]({plot_plot_years_trend_cities_path})\n\n")

        ## Literature
        ### Plot - years trend
        f.write("### Trend Publikacji Naukowych \n\n")
        f.write("Poniższy wykres ilustruje liczbę publikacji na temat zanieczyszczenia powietrza w poszczególnych latach:\n\n")
        plot_papers_per_year_path = 'report_files/papers_per_year.png'
        f.write(f"![Trend publikacji naukowych]({plot_papers_per_year_path})\n\n")


        


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