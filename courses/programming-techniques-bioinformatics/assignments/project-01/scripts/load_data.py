
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

def clean_gios_data2(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean GIOŚ PM2.5 data (new format: 2018+).

    - Automatically finds the 'Kod stacji' header row
    - Removes metadata rows (Nr, units, averaging time, etc.)
    - Converts datetime and numeric values
    - Shifts midnight (00:00) measurements to the previous day
    - Returns a clean DataFrame indexed by datetime
    """

    # Remove completely empty rows
    df = df_raw.dropna(how="all").copy()

    # Find the row that contains station codes ("Kod stacji")
    header_row_idx = df[df.iloc[:, 0] == "Kod stacji"].index[0]

    # Set column names from that row
    df.columns = df.iloc[header_row_idx]

    # Keep only rows below the header
    df = df.iloc[header_row_idx + 1 :].copy()

    # Remove metadata / non-data rows
    metadata_rows = {
        "Nr",
        "Wskaźnik",
        "Czas uśredniania",
        "Jednostka",
        "Czas pomiaru",
    }

    df = df[~df.iloc[:, 0].isin(metadata_rows)]

    # Rename datetime column and parse dates
    df.rename(columns={df.columns[0]: "Data"}, inplace=True)

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df = df[df["Data"].notna()]  # keep only valid datetime rows

    # Convert measurement values to float
    # (replace comma decimal separator)
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(
        lambda x: pd.to_numeric(
            x.astype(str).str.replace(",", "."),
            errors="coerce",
        )
    )
    # Shift midnight measurements (00:00) to the previous day
    mask_midnight = df["Data"].dt.hour == 0
    df.loc[mask_midnight, "Data"] -= pd.Timedelta(days=1)
    # Final cleanup

    df.set_index("Data", inplace=True)
    df = df.dropna(how="all", axis=0)
    df = df.astype(float)
    df.index.name = "Data"

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



#PART 5========================================

'''Creating a dictionary that maps station codes to voivodeship using 
a modified (shortened, untranslated) version of a function from 
*"wczytanie.py"* (from de Fassilier's and Rawa's repo), available here: 
https://gitlab.uw.edu.pl/d.rawa/flassilier_rawa_ztp_projekt_3'''


def pobierz_i_stworz_mapowanie_woj(url):
    
    df_meta = pd.read_excel(url)

    mapa_nazw = pd.Series(df_meta['Województwo'].values, index=df_meta['Kod stacji']).to_dict()

    return mapa_nazw








