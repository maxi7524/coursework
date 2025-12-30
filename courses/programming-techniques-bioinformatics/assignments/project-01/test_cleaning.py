import pandas as pd
from scripts.load_data import *
from scripts.analyse_data import *
import pytest

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

@pytest.fixture
def df2018_raw():
    return download_gios_archive(2018, gios_url_ids[2018], gios_pm25_file[2018])

@pytest.fixture
def df2018_clean(df2018_raw):
    return clean_gios_data2(df2018_raw)



def test_clean_gios_data_returns_dataframe(df2018_raw):
    df = clean_gios_data2(df2018_raw)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_clean_gios_data_datetime_index(df2018_raw):
    df = clean_gios_data2(df2018_raw)
    assert isinstance(df.index, pd.DatetimeIndex)


def test_clean_gios_data_numeric_columns(df2018_raw):
    df = clean_gios_data2(df2018_raw)
    assert df.dtypes.apply(lambda x: x.kind in "fi").all()


def test_no_metadata_rows(df2018_raw):
    df = clean_gios_data2(df2018_raw)
    forbidden = {"Nr", "Wskaźnik", "Czas uśredniania", "Jednostka", "Czas pomiaru"}
    assert not set(df.columns).intersection(forbidden)


def test_clean_column_names_removes_spaces():
    df = pd.DataFrame(columns=["  Abc ", "Def\n"])
    df = clean_column_names(df)
    assert "Abc" in df.columns
    assert "Def" in df.columns


def test_map_old_to_new_codes_returns_dict():
    mapping = map_old_to_new_codes()
    assert isinstance(mapping, dict)
    assert len(mapping) > 0
