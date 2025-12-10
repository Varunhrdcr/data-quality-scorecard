import numpy as np
import pandas as pd
from .dq_metrics import (
    compute_completeness,
    compute_uniqueness,
    compute_validity,
    compute_timeliness,
    compute_consistency,
)


def build_scorecard(df: pd.DataFrame) -> dict:
    completeness_df = compute_completeness(df)
    uniqueness_df = compute_uniqueness(df)
    validity_df = compute_validity(df)
    timeliness_df = compute_timeliness(df)
    consistency_df = compute_consistency(df)

    # Aggregate dimension-level scores
    scores = []

    if not completeness_df.empty:
        scores.append({
            "dimension": "Completeness",
            "score": round(completeness_df["completeness_pct"].mean(), 2),
        })

    if not uniqueness_df.empty:
        # Only consider dataset-level uniqueness for overall score
        dataset_rows = uniqueness_df[uniqueness_df["level"] == "dataset"]
        if not dataset_rows.empty:
            score = dataset_rows["uniqueness_pct"].iloc[0]
        else:
            score = uniqueness_df["uniqueness_pct"].mean()
        scores.append({
            "dimension": "Uniqueness",
            "score": round(float(score), 2),
        })

    if not validity_df.empty:
        scores.append({
            "dimension": "Validity",
            "score": round(validity_df["validity_pct"].mean(), 2),
        })

    if not timeliness_df.empty:
        scores.append({
            "dimension": "Timeliness",
            "score": round(timeliness_df["timeliness_score"].mean(), 2),
        })

    if not consistency_df.empty:
        scores.append({
            "dimension": "Consistency",
            "score": round(consistency_df["consistency_pct"].mean(), 2),
        })

    overall_df = pd.DataFrame(scores)
    if not overall_df.empty:
        overall_score = float(overall_df["score"].mean())
    else:
        overall_score = np.nan

    return {
        "completeness": completeness_df,
        "uniqueness": uniqueness_df,
        "validity": validity_df,
        "consistency": consistency_df,
        "timeliness": timeliness_df,
        "overall_scores": overall_df,
        "overall_score_value": None if np.isnan(overall_score) else round(overall_score, 2),
    }
