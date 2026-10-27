from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "social_media_posts.csv"
PROCESSED = ROOT / "data" / "processed" / "social_media_posts_clean.csv"
DB = ROOT / "data" / "social_media_analytics.db"

REQUIRED = ["post_id","post_date","platform","content_type","topic","campaign","followers",
            "reach","impressions","likes","comments","shares","saves","sentiment",
            "hashtags_count","caption_length"]
METRICS = ["followers","reach","impressions","likes","comments","shares","saves",
           "hashtags_count","caption_length"]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df = df[REQUIRED].copy()
    df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
    df = df.dropna(subset=["post_id", "post_date", "platform"])
    df["post_id"] = df["post_id"].astype(str).str.strip()
    for c in ["platform","content_type","topic","campaign","sentiment"]:
        df[c] = df[c].fillna("Unknown").astype(str).str.strip()
        df[c] = df[c].replace("", "Unknown")
    df["platform"] = df["platform"].str.title()
    df["sentiment"] = df["sentiment"].str.title()
    for c in METRICS:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        df[c] = df[c].clip(lower=0).astype(int)
    df = df.drop_duplicates(subset=["post_id"], keep="last")
    # Reach and impressions are counts; impressions should not be below reach.
    df["impressions"] = df[["impressions","reach"]].max(axis=1)
    df["total_engagement"] = df[["likes","comments","shares","saves"]].sum(axis=1)
    df["engagement_rate_pct"] = np.where(
        df["reach"] > 0, df["total_engagement"] / df["reach"] * 100, 0
    ).round(2)
    df["post_day"] = df["post_date"].dt.day_name()
    df["post_hour"] = df["post_date"].dt.hour
    df["post_month"] = df["post_date"].dt.to_period("M").astype(str)
    return df.sort_values("post_date").reset_index(drop=True)

def main():
    ROOT.joinpath("data/processed").mkdir(parents=True, exist_ok=True)
    ROOT.joinpath("data").mkdir(exist_ok=True)
    raw = pd.read_csv(RAW)
    clean = clean_data(raw)
    clean.to_csv(PROCESSED, index=False)
    with sqlite3.connect(DB) as conn:
        clean.to_sql("posts", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_posts_date ON posts(post_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform)")
    print(f"ETL complete: {len(raw)} raw rows -> {len(clean)} clean rows")
    print(f"Processed CSV: {PROCESSED}")
    print(f"SQLite DB: {DB}")

if __name__ == "__main__":
    main()
