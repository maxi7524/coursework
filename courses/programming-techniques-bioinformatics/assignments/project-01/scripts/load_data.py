
### -------------------- ###
###  Libraries
### -------------------- ### 
# Libraries
## files management
from pathlib import Path
import requests
import zipfile
import io, os
## data frameworks
import pandas as pd
import numpy as np


### -------------------- ###
###  Download  
### -------------------- ### 
# funkcja do ściągania podanego archiwum
gios_archive_url = "https://powietrze.gios.gov.pl/pjp/archives/downloadFile/"
def download_gios_archive(year, gios_id, filename):
    # Pobranie archiwum ZIP do pamięci
    url = f"{gios_archive_url}{gios_id}"
    response = requests.get(url)
    response.raise_for_status()  # jeśli błąd HTTP, zatrzymaj
    
    # Otwórz zip w pamięci
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # znajdź właściwy plik z PM2.5
        if not filename:
            print(f"Błąd: nie znaleziono {filename}.")
        else:
            # wczytaj plik do pandas
            with z.open(filename) as f:
                try:
                    df = pd.read_excel(f, header=None)
                except Exception as e:
                    print(f"Błąd przy wczytywaniu {year}: {e}")
    return df

### -------------------- ###
###  Clean data 
### -------------------- ### 
###TODO ---------- połączyć te funkcje ---------- ###
def clean_gios_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean GIOŚ PM2.5 data where 6th row contains column names.
    Removes extra header rows and unit rows, converts data to numeric,
    and sets datetime column 'Data'.
    """
   
    df = df_raw.dropna(how='all').copy()
    df.columns = df.iloc[5]

    df = df_raw.copy()
    df.columns = df.iloc[5]
    df = df.iloc[6:].copy()

    df.rename(columns={df.columns[0]: "Data"}, inplace=True)
    df = df[~df.iloc[:, 1].astype(str).str.contains('1g|ug/m3', na=False)]

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce", format="%Y-%m-%d %H:%M:%S")
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

    mask_midnight = df["Data"].dt.hour == 0
    df.loc[mask_midnight, "Data"] -= pd.Timedelta(days=1)

    df.set_index("Data", inplace=True)
    df = df.dropna(how='all', axis=0)

    df = df.astype(float)
    return df

def clean_gios_2014(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean GIOŚ PM2.5 2014-format data:
    - use first row as column headers,
    - remove metadata rows,
    - convert the first column to datetime and set as index,
     
    - convert all measurement columns to numeric.
    """
    df = df_raw.copy()
    df.columns = df.iloc[0]
    df = df.drop(index=0).reset_index(drop=True)
    df.rename(columns={df.columns[0]: "Data"}, inplace=True)
    df = df.dropna(axis=1, how='all')
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df.set_index("Data", inplace=True)
    df = df.apply(pd.to_numeric, errors="coerce")
    
    df = df.iloc[2:]
    mask_midnight = df.index.hour == 0
    df.index = df.index - pd.to_timedelta(mask_midnight.astype(int), unit="D")

    df = df.astype(float)
    return df

def clean_column_names(df):
    """Clean column names to standardize them across different years and simplify station code mapping."""
    df.columns = (
        df.columns.str.strip()
        .str.replace("-PM2.5-1g", "", regex=False)
        .str.replace(" ", "")
    )
    return df
###TODO ---------- end ---------- ###

### -------------------- ###
###  Download function 
### -------------------- ### 