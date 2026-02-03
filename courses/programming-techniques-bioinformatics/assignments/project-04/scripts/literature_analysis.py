
### -------------------- ###
###  libraries
### -------------------- ### 

# script functionality
import argparse
import yaml
from pathlib import Path

# analysis
import pandas as pd
import matplotlib.pyplot as plt

# functions from project 1 and 3  
from analyse_data import years_trend_cities

### -------------------- ###
###  Variables
### -------------------- ### 

# set path for script ()
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[0]
INPUT_DIR = PROJECT_ROOT / 'results' / 'literature'
OUTDIR_PATH = PROJECT_ROOT / 'results' / 'report_files'
OUTDIR_PATH.mkdir(parents=True, exist_ok=True)

### -------------------- ###
###  Helpers
### -------------------- ### 

def load_all_years(base_dir, years):
    dfs = []
    for y in years:
        path = base_dir / str(y) / "pubmed_papers.csv"
        if path.exists():
            df = pd.read_csv(path)
            df["year"] = int(y)
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def publications_per_year(df):
    return (
        df.groupby("year")
        .size()
        .reset_index(name="n_papers")
        .sort_values("year")
    )


def top_journals_global(df, n=10):
    return (
        df["journal"]
        .value_counts()
        .head(n)
        .reset_index()
        .rename(columns={"index": "journal", "journal": "n_papers"})
    )

def example_titles(df, n=5):
    return df["title"].dropna().head(n).tolist()

def plot_trend(df_years, outpath):
    plt.figure()
    plt.plot(df_years["year"], df_years["n_papers"], marker="o")
    plt.xlabel("Year")
    plt.ylabel("Number of publications")
    plt.title("PubMed publications over time")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

### -------------------- ###
###  main code 
### -------------------- ### 

def main(years:int) -> None:
    print("Analyze literature ...")

    # load data
    df = load_all_years(INPUT_DIR, years)
    
    # analysis part
    per_year = publications_per_year(df)
    journals = top_journals_global(df)
    titles = example_titles(df, 3)

    # save files
    per_year.to_csv(OUTDIR_PATH / 'publications_per_year.csv', index=False)
    journals.to_csv(OUTDIR_PATH / "top_journals_global.csv", index=False)

    # create abd save okit 
    plot_trend(per_year, OUTDIR_PATH / "papers_per_year.png")
        
    return per_year, journals, titles


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


    main(
        years = years
    )