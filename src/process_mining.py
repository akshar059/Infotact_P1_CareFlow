
from pathlib import Path

import pandas as pd
import pm4py

# Project folders
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "raw" / "sample_event_log.csv"
OUTPUT_FILE = ROOT / "docs" / "process_map.svg"

# 1. Read the event log
df = pd.read_csv(DATA_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# 2. Validate required columns
required_columns = {"case_id", "activity", "timestamp"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"CSV must contain: {required_columns}")

if df[list(required_columns)].isnull().any().any():
    raise ValueError("Missing values found. Clean the data first.")

# 3. Sort activities by patient and time
df = df.sort_values(["case_id", "timestamp"])

print("\n--- Patient Pathways ---")
for case_id, group in df.groupby("case_id"):
    pathway = " -> ".join(group["activity"].astype(str))
    print(f"{case_id}: {pathway}")

# 4. Discover the process map using PM4Py
event_log = pm4py.format_dataframe(
    df,
    case_id="case_id",
    activity_key="activity",
    timestamp_key="timestamp",
)

dfg, start_activities, end_activities = pm4py.discover_dfg(
    event_log,
    case_id_key="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp",
)

print("\n--- Process Mining Results ---")
print("Start activities:", start_activities)
print("End activities:", end_activities)
print("Activity transitions and their frequencies:")
for (source, target), count in dfg.items():
    print(f"{source} -> {target}: {count}")

# 5. Save the process map
try:
    pm4py.save_vis_dfg(
        dfg,
        start_activities,
        end_activities,
        str(OUTPUT_FILE),
    )
    print(f"\nProcess map saved to: {OUTPUT_FILE}")
except Exception as error:
    print("\nCould not create the process map.")
    print("Check whether Graphviz is installed and available in PATH.")
    print("Details:", error)
