
### -------------------- ###
###  libraries
### -------------------- ### 

# script functionality
import argparse
import yaml
import pandas as pd
from pathlib import Path
from Bio import Entrez

from functools import reduce


# functions from project 1 and 3  
from analyse_data import years_trend_cities

### -------------------- ###
###  Variables
### -------------------- ### 

# set path for script ()
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[0]
OUTDIR_PATH = PROJECT_ROOT / 'results' / 'literature'
OUTDIR_PATH.mkdir(parents=True, exist_ok=True)

### -------------------- ###
###  Helpers
### -------------------- ### 

def pubmed_search(query, year, retmax):
    '''
    Function return pubmed ids for related articles for given query and year
    '''
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        mindate=str(year),
        maxdate=str(year),
        datetype="pdat", # publication date
        retmax=retmax, # default 20
        sort="pub_date" # deterministic approach - sorted results will always be returned in same order
    )
    record = Entrez.read(handle)
    return record["IdList"]


def fetch_summaries(pmids):
    '''
    Function takes ids from pubmed and metadata summaries for them
    
    :param pmids: dict  with pubmed ids
    '''

    handle = Entrez.esummary(db="pubmed", id=",".join(pmids))
    return Entrez.read(handle)


def normalize_records(records):
    '''
    It returns df with interpretable names
    
    :param records: dict from readed esummary files, 
    '''
    rows = []
    for r in records:
        rows.append({
            "pmid": r["Id"],
            "title": r.get("Title", ""),
            "journal": r.get("FullJournalName", ""),
            "year": r.get("PubDate", "")[:4],
            "authors": "; ".join(a["Name"] for a in r.get("Authors", []))
        })
    return pd.DataFrame(rows)


def aggregate_by_year(df):
    return (
        df.groupby("year")
        .size()
        .reset_index(name="n_papers")
    )


def top_journals(df, n=10):
    return (
        df["journal"]
        .value_counts()
        .head(n)
        .reset_index(name="n_papers")
        .rename(columns={"index": "journal"})
    )

### -------------------- ###
###  main code 
### -------------------- ### 

def main(year:int, entrez_mail: str, query: str, retmax: 200) -> None:
    print(f"Get literature data from {year}")

    # file paths
    outdir = Path(OUTDIR_PATH / f"{year}")
    outdir.mkdir(parents=True, exist_ok=True)
    
    # Entrez part 
    Entrez.email = entrez_mail
    pmids = pubmed_search(query, year, retmax)
    summaries = fetch_summaries(pmids)
    df = normalize_records(summaries)

    # Save results
    df.to_csv(outdir / "pubmed_papers.csv", index=False)
    aggregate_by_year(df).to_csv(outdir / "summary_by_year.csv", index=False)
    top_journals(df).to_csv(outdir / "top_journals.csv", index=False)
    
    pass


if __name__ == "__main__":
    # args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=str, required=True)
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
        year=args.year, 
        entrez_mail=entrez_mail,
        query=query,
        retmax=retmax,
    )