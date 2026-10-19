
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "patient_waiting_time_summary.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)

# Validate required columns
required = {"case_id", "activity_name", "activity_order", "timestamp"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

if df[list(required)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# Parse timestamps and order activities for each patient
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
df = df.sort_values(["case_id", "activity_order"]).copy()

# Get previous activity and timestamp within each case
df["previous_activity"] = df.groupby("case_id")["activity_name"].shift(1)
df["previous_timestamp"] = df.groupby("case_id")["timestamp"].shift(1)

# Calculate elapsed time between consecutive recorded activities
df["waiting_time_minutes"] = (
    df["timestamp"] - df["previous_timestamp"]
).dt.total_seconds() / 60

# Keep transitions where a previous activity exists
transitions = df.dropna(subset=["previous_activity"]).copy()

# Summarize elapsed time by activity transition
summary = (
    transitions.groupby(["previous_activity", "activity_name"])
    .agg(
        transition_count=("waiting_time_minutes", "size"),
        average_minutes=("waiting_time_minutes", "mean"),
        median_minutes=("waiting_time_minutes", "median"),
        maximum_minutes=("waiting_time_minutes", "max"),
    )
    .reset_index()
    .rename(columns={
        "previous_activity": "from_activity",
        "activity_name": "to_activity",
    })
)

time_columns = ["average_minutes", "median_minutes", "maximum_minutes"]
summary[time_columns] = summary[time_columns].round(2)
summary = summary.sort_values("average_minutes", ascending=False)

# Save summary
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT_FILE, index=False)

print("=== PATIENT WAITING TIME ANALYSIS ===")
print(f"Total patient cases: {df['case_id'].nunique()}")
print(f"Total recorded events: {len(df)}")
print(f"Transitions analysed: {len(transitions)}")
print("\nTop 10 transitions by average elapsed time:")
print(summary.head(10).to_string(index=False))
print(f"\nResults saved to: {OUTPUT_FILE}")
print("\nNote: Elapsed time is not necessarily actual waiting time.")
