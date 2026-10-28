
from pathlib import Path

import pandas as pd
import streamlit as st

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

ACTIVITY_FILE = DATA_DIR / "activity_frequency_summary.csv"
PATHWAY_FILE = DATA_DIR / "patient_journey_sequence_summary.csv"
PERFORMANCE_FILE = DATA_DIR / "workflow_performance_summary.csv"

st.set_page_config(
    page_title="CareFlow Dashboard",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 CareFlow Patient Workflow Dashboard")
st.caption("Process Mining & Workflow Analysis | Day 17")

@st.cache_data
def load_data():
    required_files = [ACTIVITY_FILE, PATHWAY_FILE, PERFORMANCE_FILE]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(f"Required file not found: {file_path}")

    activity = pd.read_csv(ACTIVITY_FILE)
    pathways = pd.read_csv(PATHWAY_FILE)
    performance = pd.read_csv(PERFORMANCE_FILE)

    return activity, pathways, performance


def find_column(df, candidates):
    normalized = {
        str(col).strip().lower().replace("_", " "): col
        for col in df.columns
    }

    for candidate in candidates:
        key = candidate.lower().replace("_", " ")
        if key in normalized:
            return normalized[key]

    for col in df.columns:
        key = str(col).strip().lower().replace("_", " ")
        if any(candidate.lower().replace("_", " ") in key
               for candidate in candidates):
            return col

    raise ValueError(
        f"Could not find columns {candidates}. "
        f"Available columns: {list(df.columns)}"
    )


try:
    activity_df, pathway_df, performance_df = load_data()

    # Identify activity summary columns
    activity_name_col = find_column(
        activity_df, ["activity_name", "activity"]
    )
    activity_count_col = find_column(
        activity_df,
        ["event_count", "activity_count", "frequency", "count", "events"]
    )

    # Identify pathway summary columns
    pathway_name_col = find_column(
        pathway_df,
        ["activity_sequence", "journey_sequence", "pathway", "sequence"]
    )
    pathway_count_col = find_column(
        pathway_df,
        ["case_count", "patient_count", "frequency", "count", "cases"]
    )

    # Identify performance summary columns
    from_col = find_column(
        performance_df, ["from_activity", "source_activity", "from"]
    )
    to_col = find_column(
        performance_df, ["to_activity", "target_activity", "to"]
    )
    elapsed_col = find_column(
        performance_df,
        [
            "average_elapsed_minutes",
            "avg_elapsed_minutes",
            "mean_elapsed_minutes",
        ],
    )

    activity_df[activity_count_col] = pd.to_numeric(
        activity_df[activity_count_col], errors="coerce"
    )
    pathway_df[pathway_count_col] = pd.to_numeric(
        pathway_df[pathway_count_col], errors="coerce"
    )
    performance_df[elapsed_col] = pd.to_numeric(
        performance_df[elapsed_col], errors="coerce"
    )

    activity_df = activity_df.dropna(subset=[activity_count_col])
    pathway_df = pathway_df.dropna(subset=[pathway_count_col])
    performance_df = performance_df.dropna(subset=[elapsed_col])

    # Dashboard summary metrics
    total_events = int(activity_df[activity_count_col].sum())
    total_activity_types = len(activity_df)
    total_pathways = len(pathway_df)
    total_transitions = len(performance_df)

    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric("Recorded Events", f"{total_events:,}")
    metric2.metric("Activity Types", total_activity_types)
    metric3.metric("Observed Pathways", total_pathways)
    metric4.metric("Transition Types", total_transitions)

    st.divider()

    # Activity frequency chart
    st.subheader("1. Activity Frequency")
    activity_chart = activity_df.sort_values(
        activity_count_col, ascending=False
    ).set_index(activity_name_col)[[activity_count_col]]
    st.bar_chart(activity_chart)
    st.caption("Shows recorded event counts for each activity.")

    # Patient pathway chart
    st.subheader("2. Patient Journey Pathways")
    pathway_display = pathway_df.nlargest(
        6, pathway_count_col
    ).copy()
    pathway_display["Pathway"] = [
        f"Pathway {i + 1}" for i in range(len(pathway_display))
    ]
    pathway_chart = pathway_display.set_index("Pathway")[
        [pathway_count_col]
    ]
    st.bar_chart(pathway_chart)

    st.dataframe(
        pathway_display[["Pathway", pathway_name_col, pathway_count_col]],
        width="stretch",
        hide_index=True,
    )

    # Elapsed-time chart
    st.subheader("3. Highest Average Elapsed-Time Transitions")
    performance_df["Transition"] = (
        performance_df[from_col].astype(str)
        + " → "
        + performance_df[to_col].astype(str)
    )

    top_transitions = performance_df.nlargest(
        10, elapsed_col
    ).sort_values(elapsed_col, ascending=False)

    st.bar_chart(
        top_transitions.set_index("Transition")[[elapsed_col]]
    )

    st.dataframe(
        top_transitions[["Transition", elapsed_col]],
        width="stretch",
        hide_index=True,
    )

    st.info(
        "Interpretation note: Elapsed time between recorded activities "
        "does not necessarily equal actual waiting time and does not "
        "by itself prove a bottleneck."
    )

    st.success("Dashboard data loaded successfully.")

except (FileNotFoundError, ValueError, KeyError) as error:
    st.error(f"Dashboard could not load the data: {error}")
    st.info(
        "Check that the summary CSV files exist and their column names "
        "match the expected fields."
    )
