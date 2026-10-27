from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from analysis import load_posts, platform_summary, generate_insights

st.set_page_config(page_title="Social Media Reach Analysis", page_icon="📊", layout="wide")
st.title("📊 Social Media Reach Analysis")
st.caption("End-to-end analytics: reach, impressions, engagement, content performance and actionable insights.")

try:
    df = load_posts()
except FileNotFoundError:
    st.error("Analytics database not found. Run `python src/etl.py` in the project folder first.")
    st.stop()

with st.sidebar:
    st.header("Filters")
    platforms = st.multiselect("Platform", sorted(df["platform"].unique()), default=sorted(df["platform"].unique()))
    content_types = st.multiselect("Content type", sorted(df["content_type"].unique()), default=sorted(df["content_type"].unique()))
    topics = st.multiselect("Topic", sorted(df["topic"].unique()), default=sorted(df["topic"].unique()))
    min_date = df["post_date"].min().date()
    max_date = df["post_date"].max().date()
    date_range = st.date_input("Post date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = df[df["platform"].isin(platforms) & df["content_type"].isin(content_types) & df["topic"].isin(topics)].copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[(filtered["post_date"].dt.date >= date_range[0]) & (filtered["post_date"].dt.date <= date_range[1])]

if filtered.empty:
    st.warning("No posts match these filters. Adjust the selections in the sidebar.")
    st.stop()

total_reach = int(filtered["reach"].sum())
total_impressions = int(filtered["impressions"].sum())
total_engagement = int(filtered["total_engagement"].sum())
avg_rate = float(filtered["engagement_rate_pct"].mean())
c1,c2,c3,c4 = st.columns(4)
c1.metric("Posts analyzed", f"{len(filtered):,}")
c2.metric("Total reach", f"{total_reach:,}")
c3.metric("Total impressions", f"{total_impressions:,}")
c4.metric("Avg. engagement rate", f"{avg_rate:.2f}%")

tab1,tab2,tab3,tab4 = st.tabs(["Overview","Platform analysis","Content & timing","Data explorer"])
with tab1:
    left,right = st.columns(2)
    monthly = filtered.assign(month=filtered["post_date"].dt.to_period("M").astype(str)).groupby("month",as_index=False).agg(reach=("reach","sum"), engagement=("total_engagement","sum"))
    left.plotly_chart(px.line(monthly,x="month",y="reach",markers=True,title="Monthly reach trend"), use_container_width=True)
    right.plotly_chart(px.scatter(filtered,x="reach",y="total_engagement",color="platform",hover_data=["post_id","content_type"],title="Reach vs total engagement"), use_container_width=True)
    st.subheader("Automated insights")
    for insight in generate_insights(filtered):
        st.write("• " + insight)
with tab2:
    summary = platform_summary(filtered)
    st.dataframe(summary, use_container_width=True, hide_index=True)
    left,right = st.columns(2)
    left.plotly_chart(px.bar(summary,x="platform",y="reach",title="Total reach by platform",color="platform"),use_container_width=True)
    right.plotly_chart(px.bar(summary,x="platform",y="avg_engagement_rate",title="Average engagement rate (%)",color="platform"),use_container_width=True)
with tab3:
    by_type = filtered.groupby("content_type",as_index=False).agg(posts=("post_id","count"), avg_rate=("engagement_rate_pct","mean"), total_reach=("reach","sum")).sort_values("avg_rate",ascending=False)
    left,right = st.columns(2)
    left.plotly_chart(px.bar(by_type,x="content_type",y="avg_rate",title="Average engagement rate by content type"),use_container_width=True)
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    by_day = filtered.groupby("post_day",as_index=False).agg(avg_rate=("engagement_rate_pct","mean"))
    by_day["post_day"] = pd.Categorical(by_day["post_day"], categories=day_order, ordered=True)
    by_day = by_day.sort_values("post_day")
    right.plotly_chart(px.bar(by_day,x="post_day",y="avg_rate",title="Average engagement rate by day"),use_container_width=True)
    st.dataframe(by_type, use_container_width=True, hide_index=True)
with tab4:
    st.write("Cleaned records currently in the analytics database.")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), "social_media_filtered.csv", "text/csv")
    st.download_button("Download platform summary as CSV", platform_summary(filtered).to_csv(index=False).encode("utf-8"), "platform_summary.csv", "text/csv")

st.caption("Dataset is synthetic demonstration data. Replace it with properly licensed real data before making real-world business claims.")
