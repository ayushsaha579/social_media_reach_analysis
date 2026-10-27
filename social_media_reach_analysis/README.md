# Social Media Reach Analysis

An end-to-end portfolio project that demonstrates data ingestion, data cleaning, validation, SQLite storage, SQL analytics, Python analysis, an interactive Streamlit dashboard, automated descriptive insights, testing, and CSV exports.

## Important data note
`data/raw/social_media_posts.csv` is a **synthetic dataset generated for this project**. It is not data collected from real social media accounts and should not be presented as real-world evidence. Replace it with a properly licensed dataset or authorized platform exports for real-world conclusions.

## Features
- ETL pipeline with type conversion, null handling, duplicate removal, non-negative metric validation, and derived engagement metrics.
- SQLite database with indexes.
- SQL queries for platform, content type, time, sentiment, and top-post analysis.
- Interactive dashboard with filters, KPI cards, Plotly charts, automated insights, and CSV downloads.
- Unit tests for core cleaning behavior.

## Project structure
```text
social_media_reach_analysis/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/social_media_posts.csv
│   ├── processed/social_media_posts_clean.csv  # created by ETL
│   └── social_media_analytics.db               # created by ETL
├── src/
│   ├── etl.py
│   └── analysis.py
├── sql/analysis_queries.sql
├── tests/test_etl.py
└── reports/
```

## Setup (Windows PowerShell)
Use a supported Python version installed on your computer. A Python 3.11–3.13 environment is a safe choice for broad package compatibility.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you can use the environment's executable directly:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the pipeline and dashboard
From the project root folder:
```powershell
python src/etl.py
streamlit run app.py
```
The dashboard should open in your browser. The database and processed CSV are created by the ETL step.

## Run tests
```powershell
pytest -q
```

## Metrics
- Total reach: sum of the reach values across posts. This is **not deduplicated unique audience reach** across posts.
- Impressions: total displays.
- Total engagement: likes + comments + shares + saves.
- Engagement rate (%): total engagement divided by reach, multiplied by 100.
- Average engagement rate: arithmetic mean of per-post engagement rates. This differs from aggregate engagement divided by aggregate reach.

Reach and impressions may have different definitions across platforms. Compare them carefully and document the definition used.

## Suggested analysis questions
1. Which platform has the highest total reach?
2. Which platform has the highest average engagement rate?
3. Which content type performs best on engagement rate?
4. How does reach change month by month?
5. Which days show higher engagement in this dataset?
6. Does hashtag count appear associated with engagement?
7. Which posts have high reach but low engagement?
8. How does sentiment distribution vary across topics?

## Portfolio upgrades
- Add a Power BI dashboard.
- Add scheduled ETL and structured logging.
- Add schema validation with Pandera.
- Add data-quality and pipeline-run tables.
- Add an experiment or forecasting model only after establishing a suitable real dataset and evaluation baseline.
- Add a deployment workflow and a clear data source/licence statement.

## Deployment
Streamlit Community Cloud can deploy an app from a GitHub repository. Follow the official instructions at https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app. Commit the source, `requirements.txt`, and a suitably sized data file. For larger or sensitive data, use suitable external storage and secrets management instead of committing it.
