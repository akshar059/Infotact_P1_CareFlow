
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = (
    ROOT / "data" / "processed" / "workflow_performance_summary.csv"
)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Validate required columns
required = {"case_id", "activity_name", "timestamp", "activity_order"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

if df[list(required)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# Convert timestamps
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

if df["timestamp"].isnull().any():
    raise ValueError("Invalid timestamps found in the dataset.")

# Sort activities for each patient
df = df.sort_values(["case_id", "activity_order"]).copy()

# Find the next activity and timestamp
df["next_activity"] = df.groupby("case_id")["activity_name"].shift(-1)
df["next_timestamp"] = df.groupby("case_id")["timestamp"].shift(-1)

# Calculate elapsed time in minutes
df["elapsed_minutes"] = (
    df["next_timestamp"] - df["timestamp"]
).dt.total_seconds() / 60

transitions = df.dropna(
    subset=["next_activity", "next_timestamp"]
).copy()

# Exclude negative elapsed intervals
transitions = transitions[
    transitions["elapsed_minutes"] >= 0
].copy()

# Summarize transition performance
summary = (
    transitions.groupby(["activity_name", "next_activity"])
    .agg(
        transition_count=("elapsed_minutes", "size"),
        average_elapsed_minutes=("elapsed_minutes", "mean"),
        median_elapsed_minutes=("elapsed_minutes", "median"),
        maximum_elapsed_minutes=("elapsed_minutes", "max"),
    )
    .reset_index()
)

summary = summary.rename(columns={
    "activity_name": "from_activity",
    "next_activity": "to_activity",
})

summary["average_elapsed_minutes"] = (
    summary["average_elapsed_minutes"].round(2)
)
summary["median_elapsed_minutes"] = (
    summary["median_elapsed_minutes"].round(2)
)
summary["maximum_elapsed_minutes"] = (
    summary["maximum_elapsed_minutes"].round(2)
)

# Rank by average elapsed time
summary = summary.sort_values(
    "average_elapsed_minutes",
    ascending=False
).reset_index(drop=True)

summary.insert(0, "rank_by_average_elapsed", range(1, len(summary) + 1))

# Add frequency rank
frequency_ranks = summary["transition_count"].rank(
    method="dense", ascending=False
).astype(int)

summary["frequency_rank"] = frequency_ranks

# Save summary
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT_FILE, index=False)

print("=== WORKFLOW PERFORMANCE SUMMARY ===")
print(f"Total patient cases: {df['case_id'].nunique()}")
print(f"Total recorded events: {len(df)}")
print(f"Valid transitions analyzed: {len(transitions)}")
print(f"Unique transition types: {len(summary)}")

print("\nTop 10 transitions by average elapsed time:")
print(summary.head(10).to_string(index=False))

print("\nTop 5 most frequent transitions:")
print(
    summary.sort_values("transition_count", ascending=False)
    .head(5)
    .to_string(index=False)
)

print(f"\nResults saved to: {OUTPUT_FILE}")
print(
    "\nNote: Elapsed time is the time between recorded activities. "
    "It does not independently confirm a bottleneck."
)
