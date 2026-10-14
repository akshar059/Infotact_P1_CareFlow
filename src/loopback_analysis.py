from pathlib import Path

import pandas as pd

# Project paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load the final dataset
df = pd.read_csv(INPUT_FILE)

# Validate required columns
required = {
    "case_id",
    "activity_name",
    "activity_order",
    "is_loopback_event",
    "is_repeat_activity",
}

missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

# Sort activities within each patient case
df = df.sort_values(["case_id", "activity_order"]).copy()

# 1. Save loopback events
loopbacks = df[
    df["is_loopback_event"].astype(str).str.lower().eq("true")
].copy()

loopbacks.to_csv(
    OUTPUT_DIR / "loopback_events.csv",
    index=False,
)

# 2. Count loopbacks by activity
activity_summary = (
    loopbacks.groupby("activity_name")
    .size()
    .reset_index(name="loopback_event_count")
    .sort_values("loopback_event_count", ascending=False)
)

activity_summary.to_csv(
    OUTPUT_DIR / "loopback_activity_summary.csv",
    index=False,
)

# 3. Count cases containing at least one loopback
case_summary = (
    loopbacks.groupby("case_id")
    .size()
    .reset_index(name="loopback_event_count")
    .sort_values("loopback_event_count", ascending=False)
)

case_summary.to_csv(
    OUTPUT_DIR / "loopback_case_summary.csv",
    index=False,
)

# 4. Count repeated activities
repeats = df[
    df["is_repeat_activity"].astype(str).str.lower().eq("true")
].copy()

repeat_summary = (
    repeats.groupby("activity_name")
    .size()
    .reset_index(name="repeat_event_count")
    .sort_values("repeat_event_count", ascending=False)
)

repeat_summary.to_csv(
    OUTPUT_DIR / "repeat_activity_summary.csv",
    index=False,
)

# Display results
print("=== LOOPBACK ANALYSIS ===")
print(f"Total events: {len(df)}")
print(f"Loopback events: {len(loopbacks)}")
print(f"Cases with loopbacks: {loopbacks['case_id'].nunique()}")

print("\nLoopbacks by activity:")
print(activity_summary.to_string(index=False))

print("\nMost frequent repeated activities:")
print(repeat_summary.to_string(index=False))

print(f"\nAnalysis results saved in: {OUTPUT_DIR}")