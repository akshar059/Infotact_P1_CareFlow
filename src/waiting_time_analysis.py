from pathlib import Path

import pandas as pd

# Project paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "raw" / "sample_event_log.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load event log
df = pd.read_csv(INPUT_FILE)

# 2. Validate required columns
required_columns = {"case_id", "activity", "timestamp"}

if not required_columns.issubset(df.columns):
    raise ValueError("CSV must contain case_id, activity, timestamp.")

if df[list(required_columns)].isnull().any().any():
    raise ValueError("Missing values found in the event log.")

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
df = df.sort_values(["case_id", "timestamp"]).copy()

# 3. Calculate time between consecutive activities
df["next_activity"] = df.groupby("case_id")["activity"].shift(-1)
df["next_timestamp"] = df.groupby("case_id")["timestamp"].shift(-1)

df["elapsed_minutes"] = (
    df["next_timestamp"] - df["timestamp"]
).dt.total_seconds() / 60

# Save activity-to-activity elapsed times
transitions = df.dropna(subset=["next_activity"]).copy()
transitions["transition"] = (
    transitions["activity"] + " -> " + transitions["next_activity"]
)

transitions.to_csv(
    OUTPUT_DIR / "activity_elapsed_times.csv",
    index=False,
)

# 4. Summarize elapsed time for each transition
transition_summary = (
    transitions.groupby("transition")["elapsed_minutes"]
    .agg(["count", "mean", "max"])
    .reset_index()
)

transition_summary.columns = [
    "transition",
    "observations",
    "average_elapsed_minutes",
    "maximum_elapsed_minutes",
]

transition_summary = transition_summary.sort_values(
    "average_elapsed_minutes", ascending=False
)

transition_summary.to_csv(
    OUTPUT_DIR / "transition_waiting_summary.csv",
    index=False,
)

# 5. Calculate total journey duration per patient
patient_summary = (
    df.groupby("case_id")["timestamp"]
    .agg(first_activity="min", last_activity="max")
    .reset_index()
)

patient_summary["journey_duration_minutes"] = (
    patient_summary["last_activity"] - patient_summary["first_activity"]
).dt.total_seconds() / 60

patient_summary.to_csv(
    OUTPUT_DIR / "patient_journey_summary.csv",
    index=False,
)

# 6. Display results
print("\n--- Patient Journey Duration ---")
print(patient_summary.to_string(index=False))

print("\n--- Activity Transition Elapsed Times ---")
print(transition_summary.to_string(index=False))

print("\nAnalysis completed successfully!")
print(f"Results saved in: {OUTPUT_DIR}")