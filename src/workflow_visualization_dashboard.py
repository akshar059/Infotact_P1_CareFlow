
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Input files
activity_file = DATA_DIR / "activity_frequency_summary.csv"
pathway_file = DATA_DIR / "patient_journey_sequence_summary.csv"
elapsed_file = DATA_DIR / "workflow_performance_summary.csv"

# Load and validate input files
for file_path in [activity_file, pathway_file, elapsed_file]:
    if not file_path.exists():
        raise FileNotFoundError(f"Required analysis file not found: {file_path}")

activity_df = pd.read_csv(activity_file)
pathway_df = pd.read_csv(pathway_file)
elapsed_df = pd.read_csv(elapsed_file)

print("Loaded activity, pathway, and performance summaries.")
print(f"Activity summary rows: {len(activity_df)}")
print(f"Patient pathway rows: {len(pathway_df)}")
print(f"Workflow performance rows: {len(elapsed_df)}")


def find_column(df, candidates):
    """Find a column using common naming variations."""
    normalized = {str(col).strip().lower(): col for col in df.columns}

    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]

    for col in df.columns:
        normalized_col = str(col).strip().lower().replace("_", " ")
        if any(candidate.lower() in normalized_col for candidate in candidates):
            return col

    raise ValueError(
        f"Could not find a column matching {candidates}. "
        f"Available columns: {list(df.columns)}"
    )


# Chart 1: Activity frequency
activity_col = find_column(
    activity_df, ["activity_name", "activity", "activity name"]
)
count_col = find_column(
    activity_df, ["event_count", "frequency", "activity_count", "count", "events"]
)

activity_df[count_col] = pd.to_numeric(
    activity_df[count_col], errors="coerce"
)
activity_df = activity_df.dropna(subset=[count_col])
activity_df = activity_df.sort_values(count_col, ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(activity_df[activity_col].astype(str), activity_df[count_col])
ax.set_title("CareFlow: Activity Frequency")
ax.set_xlabel("Recorded events")
ax.set_ylabel("Activity")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "activity_frequency_chart.png", dpi=150)
plt.close(fig)

# Chart 2: Most common patient pathways
sequence_col = find_column(
    pathway_df,
    ["activity_sequence", "journey_sequence", "pathway", "sequence"]
)
pathway_count_col = find_column(
    pathway_df, ["case_count", "patient_count", "frequency", "count", "cases"]
)

pathway_df[pathway_count_col] = pd.to_numeric(
    pathway_df[pathway_count_col], errors="coerce"
)
pathway_df = pathway_df.dropna(subset=[pathway_count_col])
pathway_df = pathway_df.nlargest(6, pathway_count_col).sort_values(
    pathway_count_col, ascending=True
)

# Short labels keep long activity sequences readable.
pathway_labels = [
    f"Pathway {i + 1}" for i in range(len(pathway_df))
]

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(pathway_labels, pathway_df[pathway_count_col])
ax.set_title("CareFlow: Most Common Patient Pathways")
ax.set_xlabel("Number of patient cases")
ax.set_ylabel("Pathway")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "patient_pathway_chart.png", dpi=150)
plt.close(fig)

# Save pathway labels and their sequences for reference.
pathway_details = pathway_df[[sequence_col, pathway_count_col]].copy()
pathway_details.insert(0, "pathway_label", pathway_labels)
pathway_details.to_csv(
    DATA_DIR / "workflow_visualization_pathway_details.csv",
    index=False
)

# Chart 3: Highest average elapsed-time transitions
from_col = find_column(
    elapsed_df, ["from_activity", "source_activity", "from"]
)
to_col = find_column(
    elapsed_df, ["to_activity", "target_activity", "to"]
)
elapsed_col = find_column(
    elapsed_df,
    ["average_elapsed_minutes", "avg_elapsed_minutes", "mean_elapsed_minutes"]
)

elapsed_df[elapsed_col] = pd.to_numeric(
    elapsed_df[elapsed_col], errors="coerce"
)
elapsed_df = elapsed_df.dropna(subset=[elapsed_col])
elapsed_df = elapsed_df.nlargest(10, elapsed_col).sort_values(
    elapsed_col, ascending=True
)

transition_labels = (
    elapsed_df[from_col].astype(str)
    + " → "
    + elapsed_df[to_col].astype(str)
)

fig, ax = plt.subplots(figsize=(11, 7))
ax.barh(transition_labels, elapsed_df[elapsed_col])
ax.set_title("CareFlow: Highest Average Elapsed-Time Transitions")
ax.set_xlabel("Average elapsed time (minutes)")
ax.set_ylabel("Activity transition")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "workflow_elapsed_time_chart.png", dpi=150)
plt.close(fig)

print("\nDashboard charts created successfully:")
print(OUTPUT_DIR / "activity_frequency_chart.png")
print(OUTPUT_DIR / "patient_pathway_chart.png")
print(OUTPUT_DIR / "workflow_elapsed_time_chart.png")
print(DATA_DIR / "workflow_visualization_pathway_details.csv")
print(
    "\nNote: Elapsed time between recorded activities does not "
    "necessarily represent actual waiting time or prove a bottleneck."
)
