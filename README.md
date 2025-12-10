# Data Quality Scorecard Automation

A small hackathon-ready project to generate a **data quality scorecard** for a tabular dataset.

## Features

- Completeness → % non-null per column  
- Uniqueness → duplicate vs distinct (primary key + per column)  
- Validity → generic non-null / non-empty checks  
- Consistency → simple cross-column rule example  
- Timeliness → freshness of date columns based on configurable thresholds  
- Streamlit dashboard for quick visualization

## Project Structure

```text
dq_scorecard/
├─ data/
│  └─ Transaction_ID,Date,Store_Location,.xlsx
├─ src/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ data_loader.py
│  ├─ dq_metrics.py
│  ├─ scorecard.py
│  └─ app.py
├─ requirements.txt
└─ README.md
