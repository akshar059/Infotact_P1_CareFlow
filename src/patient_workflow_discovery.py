from pathlib import Path
import pandas as pd
import pm4py

# Project paths
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = ROOT / "docs" / "patient_workflow_map.svg"

# 1. Load final CareFlow dataset
df = pd.read_csv(DATA_FILE)

# 2. Validate required columns
required_columns = {"case_id", "activity_name", "timestamp", "activity_order"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

if df[list(required_columns)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# 3. Prepare the event log
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
df = df.sort_values(["case_id", "activity_order"]).copy()

event_log = pm4py.format_dataframe(
    df,
    case_id="case_id",
    activity_key="activity_name",
    timestamp_key="timestamp",
)

# 4. Discover process flow
dfg, start_activities, end_activities = pm4py.discover_dfg(
    event_log,
    case_id_key="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp",
)

# 5. Display results
print("=== PATIENT WORKFLOW DISCOVERY ===")
print(f"Total events: {len(df)}")
print(f"Unique patient cases: {df['case_id'].nunique()}")
print("\nStart activities:")
print(start_activities)
print("\nEnd activities:")
print(end_activities)

print("\nActivity transitions:")
for (source, target), count in sorted(
    dfg.items(), key=lambda item: item[1], reverse=True
):
    print(f"{source} -> {target}: {count}")

# 6. Save the process map
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

pm4py.save_vis_dfg(
    dfg,
    start_activities,
    end_activities,
    str(OUTPUT_FILE),
)

print(f"\nProcess map saved to: {OUTPUT_FILE}")