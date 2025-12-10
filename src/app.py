import streamlit as st
import pandas as pd

# 🔴 IMPORTANT: no dot here!
from data_loader import load_dataset
from dq_metrics import build_scorecard


st.set_page_config(
    page_title="Data Quality Scorecard",
    layout="wide",
)


def main():
    st.title("📊 Data Quality Scorecard Automation")

    st.markdown(
        """
This app loads **load_dataset.xlsx** from the `data/` folder and calculates:

- ✅ Completeness
- 🧬 Uniqueness
- ✅ Validity
- ⏱ Timeliness

You can reuse this for any similar dataset by just replacing the Excel file.
"""
    )

    # --- Load dataset ---
    try:
        df = load_dataset()
        st.success("Dataset loaded successfully: `load_dataset.xlsx`")
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()

    # Show raw data
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df, use_container_width=True)

    # --- Build scorecard ---
    scorecard = build_scorecard(df)

    st.header("📌 Data Quality Dimensions")

    # Completeness & Uniqueness side-by-side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Completeness")
        st.dataframe(scorecard["Completeness"], use_container_width=True)

    with col2:
        st.subheader("🧬 Uniqueness")
        st.dataframe(scorecard["Uniqueness"], use_container_width=True)

    # Validity
    st.subheader("✅ Validity")
    st.dataframe(scorecard["Validity"], use_container_width=True)

    # Timeliness
    st.subheader("⏱ Timeliness")
    st.dataframe(scorecard["Timeliness"], use_container_width=True)

    st.markdown("---")
    st.caption("Hackathon – Data Quality Scorecard Automation")


if __name__ == "__main__":
    main()
