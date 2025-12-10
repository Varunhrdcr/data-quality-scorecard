from pathlib import Path

# Base directory of the project (dq_scorecard/)
BASE_DIR = Path(__file__).resolve().parents[1]

# Path to your provided dataset
DATA_FILE = BASE_DIR / "Data" / "load_dataset.xlsx"

# Column configuration (you can tweak this if dataset changes)
PRIMARY_KEY_COLS = ["Transaction_ID"]

# Date columns and freshness rules (in days)
DATE_COL_CONFIG = {
    "Date": {
        "freshness_days": 30  # e.g., data is considered fresh if latest date <= 30 days old
    }
}

# You can define basic validity rules here if needed
# For hackathon, we keep it generic and simple
VALIDITY_RULES = {
    # Example structure (not strictly used yet, but ready to be extended)
    # "Transaction_ID": {"type": "numeric_positive"},
    # "Store_Location": {"type": "non_empty_string"},
    # "Date": {"type": "date_not_in_future"},
}
