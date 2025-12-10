import pandas as pd
from datetime import datetime, timedelta


def completeness_score(df: pd.DataFrame) -> pd.DataFrame:
    
    completeness = df.notnull().mean() * 100
    return completeness.round(2).rename("Completeness (%)").to_frame()


def uniqueness_score(df: pd.DataFrame) -> pd.DataFrame:
    
    if df.empty:
        unique_pct = 0.0
        dup_count = 0
    else:
        unique_rows = len(df.drop_duplicates())
        total_rows = len(df)
        unique_pct = (unique_rows / total_rows) * 100
        dup_count = total_rows - unique_rows

    return pd.DataFrame(
        {
            "Metric": ["Unique rows (%)", "Duplicate rows (count)"],
            "Value": [round(unique_pct, 2), dup_count],
        }
    )


def validity_score(df: pd.DataFrame) -> pd.DataFrame:
    
    results = []

    for col in df.columns:
        series = df[col]
        non_null = series.dropna()
        if non_null.empty:
            results.append((col, "N/A", 0.0))
            continue

        valid_pct = 0.0
        rule = ""

        if pd.api.types.is_numeric_dtype(non_null):
            valid = non_null.between(0, 1e12)
            valid_pct = (valid.mean() * 100).round(2)
            rule = "0 <= value <= 1e12"
        else:
            # Try parsing as date
            try:
                parsed = pd.to_datetime(non_null, errors="coerce")
                valid = parsed.notna()
                valid_pct = (valid.mean() * 100).round(2)
                rule = "Parsable as datetime"
            except Exception:
                # For other types, we just set N/A for now
                rule = "No generic rule"

        results.append((col, rule, valid_pct))

    return pd.DataFrame(results, columns=["Column", "Rule", "Validity (%)"])


def timeliness_score(df: pd.DataFrame, date_columns=None, days_fresh=30) -> pd.DataFrame:
    
    if date_columns is None:
        # Auto-detect likely date columns by name
        date_columns = [
            c
            for c in df.columns
            if any(k in c.lower() for k in ["date", "time", "timestamp"])
        ]

    results = []
    now = datetime.now()
    threshold = now - timedelta(days=days_fresh)

    for col in date_columns:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce")
            valid = parsed.notna()
            recent = parsed >= threshold
            if valid.sum() == 0:
                pct_recent = 0.0
            else:
                pct_recent = (recent[valid].mean() * 100).round(2)
            results.append((col, days_fresh, pct_recent))
        except Exception:
            results.append((col, days_fresh, 0.0))

    return pd.DataFrame(
        results,
        columns=["Date Column", "Freshness Window (days)", "Timeliness (%)"],
    )


def build_scorecard(df: pd.DataFrame) -> dict:
    """
    Returns a dictionary of all metrics DataFrames.
    """
    return {
        "Completeness": completeness_score(df),
        "Uniqueness": uniqueness_score(df),
        "Validity": validity_score(df),
        "Timeliness": timeliness_score(df),
    }
