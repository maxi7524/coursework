import pandas as pd
import numpy as np

from scripts.load_data import clean_gios_data


def test_returns_dataframe_with_datetime_index(sample_raw_df):
    # The cleaned output should always be a pandas DataFrame
    # indexed by datetime, because all further analysis
    # (daily aggregation, time series, trends) depends on time indexing.
    df = clean_gios_data(sample_raw_df)

    assert isinstance(df, pd.DataFrame)
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.name == "Data"


def test_no_metadata_rows(sample_raw_df):
    # Raw GIOŚ files contain metadata rows (station codes, units, indicators).
    # This test ensures that such rows are fully removed and do not appear
    # in the cleaned time index.
    df = clean_gios_data(sample_raw_df)

    forbidden = ["Kod stacji", "Wskaźnik", "Czas uśredniania", "Jednostka"]
    index_as_str = df.index.astype(str)

    for word in forbidden:
        assert not any(index_as_str.str.contains(word))


def test_midnight_shift(sample_2014_df):
    # In GIOŚ data, measurements at 00:00 represent the previous day.
    # This test verifies that midnight timestamps are correctly shifted
    # so that daily aggregation produces the correct number of days.
    df = clean_gios_data(sample_2014_df)

    assert not (df.index.hour == 0).any()


def test_number_of_stations_positive(sample_raw_df):
    # After cleaning, the dataset should contain at least one station.
    # This sanity check ensures that columns were not accidentally dropped
    # during format detection or metadata removal.
    df = clean_gios_data(sample_raw_df)

    assert df.shape[1] > 0
