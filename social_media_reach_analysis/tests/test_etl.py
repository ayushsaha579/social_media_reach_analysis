import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from etl import clean_data

def sample():
    return pd.DataFrame([{
        "post_id":"A","post_date":"2025-01-01 12:00:00","platform":"instagram",
        "content_type":"Reel","topic":None,"campaign":"Organic","followers":100,
        "reach":50,"impressions":40,"likes":-2,"comments":3,"shares":2,"saves":1,
        "sentiment":"positive","hashtags_count":4,"caption_length":100
    }])

def test_cleaning_and_derived_fields():
    result = clean_data(sample())
    assert len(result) == 1
    assert result.loc[0,"platform"] == "Instagram"
    assert result.loc[0,"topic"] == "Unknown"
    assert result.loc[0,"likes"] == 0
    assert result.loc[0,"impressions"] >= result.loc[0,"reach"]
    assert result.loc[0,"total_engagement"] == 6
    assert result.loc[0,"engagement_rate_pct"] == 12.0

def test_duplicate_ids_removed():
    df = pd.concat([sample(), sample()], ignore_index=True)
    assert len(clean_data(df)) == 1
