
from scripts.literature_pubmed_fetch import normalize_records

def test_normalize_records_single_record():
    record = {
    "Id": "12345",
    "Title": "Test paper",
    "FullJournalName": "Nature",
    "PubDate": "2020 Feb",
    "Authors": [
        {"Name": "Smith J"},
        {"Name": "Doe A"}
    ]
    }
    df = normalize_records([record])

    assert df.shape == (1, 5)
    assert df.loc[0, "pmid"] == "12345"
    assert df.loc[0, "year"] == "2020"
    assert df.loc[0, "authors"] == "Smith J; Doe A"
    

def test_normalize_missing_fields():
    record = {"Id": "1"}
    df = normalize_records([record])

    assert df.loc[0, "title"] == ""
    assert df.loc[0, "journal"] == ""
    assert df.loc[0, "authors"] == ""
