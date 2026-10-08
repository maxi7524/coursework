### -------------------- ###
###  Libraries
### -------------------- ### 
## data frameworks
import pandas as pd
import numpy as np
## Plots
import matplotlib.pyplot as plt 
import seaborn as sns 

### -------------------- ###
###  Helper functions 
### -------------------- ### 
meta = pd.read_excel("https://powietrze.gios.gov.pl/pjp/archives/downloadFile/622", header=0, engine='openpyxl')

# loading meta data 
def map_old_to_new_codes(meta=meta) -> dict:
    """
    Create a mapping from old station codes to new station codes
    using GIOŚ metadata.

    Returns
    -------
    dict
        Dictionary mapping old station codes to current station codes.
    """

    # Find the column with old station codes (more robust)
    old_col = [c for c in meta.columns if "Stary Kod stacji" in c][0]
    new_col = "Kod stacji"

    mapping = {}

    for _, row in meta.dropna(subset=[old_col]).iterrows():
        old_codes = str(row[old_col]).split(",")

        for old in old_codes:
            old = old.strip()
            if old:
                mapping[old] = row[new_col]

    return mapping


### -------------------- ###
###  Data manipulation
### -------------------- ### 

# Task 3
def fill_na(df: pd.DataFrame) ->pd.DataFrame:
    '''
    Fills NA values in df by dropping empty values
    '''
    return df.dropna()

def time_to_month(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Changes time index representation from day to month, by mean aggregating. Returns new df
    \n**df**: Dataframe with time indexes
    '''
    new_df = df.resample('MS').mean()
    return new_df

def get_stations(df: pd.DataFrame, cities: list, *, meta=meta) -> list:
    '''
    Return df with columns that met criteria
    \n**df**: Dataframe based on GIOŚ data 
    '''
    filt = meta['Miejscowość'].isin(cities)
    # filt1 = meta['Województwo'].isin(voivodeships)
    # filt = filt1 & filt
    cols_idx = meta[filt]['Kod stacji'].to_list()
    
    df_filtered = df.loc[:, df.columns.isin(cols_idx)]
    return df_filtered

# Task 4
def get_daily_mean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily mean PM2.5 values from hourly data.
    """
    daily_df = df.resample("D").mean()  
    return daily_df

def get_daily_exceedances(df: pd.DataFrame, limit: float):
    """
    Identify daily exceedances of the PM2.5 limit for each station.
    """
    daily_df = get_daily_mean(df)       
    exceedances = daily_df > limit      

    total_days_with_exceedances = exceedances.any(axis=1).sum()  

    return exceedances.sum(axis=0), total_days_with_exceedances
    # returns number of exceedance days per station, total days with exceedance

def top3_bottom3_exceedances(exc: pd.Series) -> tuple[pd.Series, pd.Series]:
    # Finds 3 stations with the highest and 3 with the lowest number of exceedance days and returns them as two Series.
    top3 = exc.sort_values(ascending=False).head(3)
    bottom3 = exc.sort_values().head(3)

    print("Top 3 stations with the most exceedance days:")
    for station, days in top3.items():
        print(f"  {station}: {days}")

    print("\nBottom 3 stations with the fewest exceedance days:")
    for station, days in bottom3.items():
        print(f"  {station}: {days}")

    return top3, bottom3


### -------------------- ###
###  Plots
### -------------------- ### 

# Task 3
def years_trend_cities(df: pd.DataFrame, cities: list, years: list, *, meta=meta, save=False) -> None:
    '''
    Draw plots how concentration of PM2.5 was changing in given year across different cities
    \n**df**: Dataframe based on GIOŚ data TODO - tutaj zmienic nazwę po funkcji 
    \n**cities**: List of cities to compare 
    \n**years**: List of years we want to compare data
    \n**meta**: Dataframe with meta information about **df**
    \n**save**: TODO If False return None, else save plots in given folder 
    '''
    # Changes time representation: per day -> per month (mean)
    df = time_to_month(df)
    
    # Changes all to all cities
    if cities == 'all':
        # finding all cities in df
        cities = meta[meta['Kod stacji'].isin(df.columns)]['Miejscowość'].to_list()
        cities = list(set(cities))
        print(f"There is {len(cities)}")

    # plots
    for year in years:
        df_loc = df[df.index.year == year]
        for city in cities:
            # Gets stations which met condition
            values = get_stations(df_loc, cities=[city], meta=meta).mean(axis=1)
            # agg for every year 
            if not values.isna().any():
                # changing values to month
                values.index = values.index.month
                values.plot(label=f'{year}: {city}', )
    plt.legend()
    plt.title(f'Mean PM2.5 concentration in {cities}')
    plt.xlabel('Month')
    plt.ylabel('Concentration of PM2.5')
    plt.ylim((0, df.mean(axis=1).max()*1.25))
    plt.show()

def years_heatmaps_cities(df: pd.DataFrame, cities: list, years: list, *, meta=meta, save=False) -> None:
    '''
    Draw heatmaps Months $\\times$ Years which shows concentration pf PM.2.5
    \n**df**: Dataframe based on GIOŚ data 
    \n**cities**: List of cities to compare 
    \n**years**: List of years we want to compare data
    \n**meta**: Dataframe with meta information about **df**
    \n**save**: TODO If False return None, else save plots in given folder 
    '''
    # Changes time representation: per day -> per month (mean)
    df = df[df.index.year.isin(years)]
    
    df = time_to_month(df)
    # Changes all to to obtain all cities
    if cities == 'all':
        # finding all cities in df
        cities = meta[meta['Kod stacji'].isin(df.columns)]['Miejscowość'].to_list()
        cities = list(set(cities))
        print(f"There is {len(cities)}")

   # plots 
    for city in cities:
        val_col = f"city_mean"
        # Gets stations which met condition
        df[val_col] = get_stations(df, cities=[city], meta=meta).mean(axis=1)
        if not df[val_col].isna().any():
            continue 
        # creating pivot table for sns.heatmap
        pivot = pd.pivot_table(df, val_col,df.index.year, df.index.month, aggfunc='mean')
        pivot.astype(float)
        # plotting pivot table
        sns.heatmap(pivot, annot=True, linewidths=0.5, cmap='rocket_r', vmin=10, vmax=50)
        plt.title(f'Mean PM2.5 concentration in {city}')
        plt.xlabel('Month')
        plt.ylabel('Year')
        #TODO skale ustawić wszędzie taką samą i inny kolor, dostosował bym ją tak, że pokazuje gdzie jest przekroczony poziom zagrażający życiu 
        plt.show()

# Task 4 
def plot_exceedance_bar(plot_df: pd.DataFrame, title: str = None):
    """
    Plot grouped bar chart of PM2.5 daily exceedances.

    Parameters:
    -----------
    plot_df : pd.DataFrame
        DataFrame where columns are stations and rows are years.
    title : str, optional
        Title of the plot. If None, a default title is used.
    """
    plt.figure(figsize=(12, 6))
    plot_df.plot(kind="bar", figsize=(12,6))
    
    if title is None:
        title = ("Number of Days with PM2.5 Exceedances\n"
                 "WHO Limit = 15 µg/m³\nTop 3 and Bottom 3 Stations: 2015, 2018, 2021 and 2024")
    plt.title(title, fontsize=12, fontweight='bold')
    plt.xlabel("Year")
    plt.ylabel("Number of exceedance days")
    plt.legend(title="Stations", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


    #PART 5======================================

'''
The function below uses dictionary with a mapping (from pobierz_i_stworz_mapowanie_woj() in "load_data.py") and applies it to the df.
It changes the station' codes to voivodeships in the columns indexes of the df.
'''

def mapuj_wojewodztwo(df_stacje, slownik_wojewodztwa):
    df_stacje.columns = [slownik_wojewodztwa.get(kolumna, kolumna) for kolumna in df_stacje.columns]
    return df_stacje

'''
funkcja z zalozenia przyjmuje df z godzinnymi pomiarami, liczy dzienne sumy, zwraca df
z informacja o tym w jak wielu dniach danego roku nastapilo przekroczenie normy who
'''

def sumuj_dni_z_przekroczeniem(df, norma):
    #grupuje df z danymi godzinowymi po roku, miesiacu i dniu - otrzymuje srednie dzienne
    df_dzienne = df.groupby([
        df.index.year,
        df.index.month,
        df.index.day
    ]).mean()

    #dla czytelnosci zmieniam nazwy kolumn powstalych po grupowaniu
    df_dzienne.index.names = ["rok", "miesiac", "dzien"]

    #df z wartosciami logicznymi - True jesli danego dnia przekroczono norme
    df_czy_ponad_norme = df_dzienne > norma

    #zliczamy liczbę dni z przekroczeniem dla każdego roku
    df_ile_dni_ponad_norme = df_czy_ponad_norme.groupby(level="rok").sum()

    return df_ile_dni_ponad_norme


'''
Funkcja rysuje wykres w zadaniu 5.
'''

def barplot_voivodeship(df, norm):
    df.T.plot(kind="bar",
        color=["darkgreen","seagreen",
           "darkseagreen","lightgreen"],
        figsize = (8,7),
        title=f"Ilości dni z przekroczeniem normy who = {norm} w województwach"
        )
    plt.xticks(rotation = 75)
    plt.tight_layout()