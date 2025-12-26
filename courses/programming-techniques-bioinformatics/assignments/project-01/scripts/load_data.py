
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
def clean_gios_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean GIOŚ PM2.5 data from various years.
    Handles both old and new formats, removes extra headers,
    converts values to float, fixes midnight timestamps.
    """

    df = df_raw.dropna(how='all').copy()
    first_cell = str(df.iloc[0, 0]).strip()

    # --- stary format (np. 2015) ---
    if first_cell == "Kod stacji":
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)

        # Znajdź pierwszy wiersz z datą w kolumnie Data
        for i, val in enumerate(df.iloc[:, 0]):
            try:
                pd.to_datetime(val)
                first_data_row = i
                break
            except Exception:
                continue

        df = df.iloc[first_data_row:].copy()
        df.rename(columns={df.columns[0]: "Data"}, inplace=True)

        # Konwersja dat i liczb
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(",", "."), errors="coerce"))

    # --- nowy format (np. 2018, 2021, 2024) ---
    elif first_cell == "Nr":
        # Kolumny z wiersza 1 (Kod stacji)
        df.columns = df.iloc[1]
        df = df.iloc[2:].copy()
        df.rename(columns={df.columns[0]: "Data"}, inplace=True)

        # Usuń wiersze nagłówków i jednostek
        df = df[~df.iloc[:, 1].astype(str).str.contains('1g|ug/m3|µg/m3', na=False)]

        # Konwersja daty i wartości liczbowych
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        df = df[df["Data"].notna()]
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(",", "."), errors="coerce"))

    else:
        raise ValueError("Unknown GIOŚ data format")

    # Korekta godzin 00:00
    mask_midnight = df["Data"].dt.hour == 0
    df.loc[mask_midnight, "Data"] -= pd.Timedelta(days=1)

    # Ustawienie indeksu i usunięcie wierszy całkowicie pusta
    df.set_index("Data", inplace=True)
    df = df.dropna(how='all', axis=0)
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