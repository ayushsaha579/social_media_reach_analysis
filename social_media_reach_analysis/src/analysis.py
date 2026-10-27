from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "social_media_analytics.db"

def load_posts():
    if not DB.exists():
        raise FileNotFoundError("Database not found. Run: python src/etl.py")
    with sqlite3.connect(DB) as conn:
        return pd.read_sql_query("SELECT * FROM posts", conn, parse_dates=["post_date"])

def platform_summary(df):
    return (df.groupby("platform", as_index=False)
            .agg(posts=("post_id","count"), reach=("reach","sum"),
                 impressions=("impressions","sum"), engagement=("total_engagement","sum"),
                 avg_engagement_rate=("engagement_rate_pct","mean"))
            .sort_values("reach", ascending=False))

def generate_insights(df):
    if df.empty:
        return ["No data available for the selected filters."]
    out = []
    p = platform_summary(df)
    top_reach = p.iloc[0]
    out.append(f"{top_reach['platform']} has the highest total reach in the selected data ({int(top_reach['reach']):,}).")
    best_rate = p.sort_values("avg_engagement_rate", ascending=False).iloc[0]
    out.append(f"{best_rate['platform']} has the highest average engagement rate ({best_rate['avg_engagement_rate']:.2f}%).")
    types = df.groupby("content_type")["engagement_rate_pct"].mean().sort_values(ascending=False)
    if not types.empty:
        out.append(f"{types.index[0]} has the highest average engagement rate by content type ({types.iloc[0]:.2f}%).")
    days = df.groupby("post_day")["engagement_rate_pct"].mean().sort_values(ascending=False)
    if not days.empty:
        out.append(f"{days.index[0]} has the highest average engagement rate by posting day ({days.iloc[0]:.2f}%).")
    out.append("These are descriptive patterns, not proof that platform or posting time caused better performance.")
    return out
