from pathlib import Path

import pandas as pd

# Project paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "raw" / "sample_event_log.csv"

# Load event log
df = pd.read_csv(INPUT_FILE)

print("=== EVENT LOG VALIDATION ===")
print(f"Total events: {len(df)}")
print(f"Total patient cases: {df['case_id'].nunique()}")

# 1. Check required columns
required_columns = {"case_id", "activity", "timestamp"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    print(f"FAIL: Missing columns: {sorted(missing_columns)}")
else:
    print("PASS: Required columns are present.")

# 2. Check missing values
if required_columns.issubset(df.columns):
    missing_values = df[list(required_columns)].isnull().sum()
    print("\nMissing values:")
    print(missing_values.to_string())

    if missing_values.sum() == 0:
        print("PASS: No missing required values.")
    else:
        print("FAIL: Missing required values found.")

    # Continue timestamp and event checks only if required data exists
    if missing_values.sum() == 0:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )

        if df["timestamp"].isnull().any():
            print("FAIL: Invalid timestamps found.")
        else:
            print("PASS: All timestamps are valid.")

            # 3. Check event order within each case
            ordered = df.sort_values(["case_id", "timestamp"])
            time_diffs = ordered.groupby("case_id")["timestamp"].diff()

            if (time_diffs.dropna() < pd.Timedelta(0)).any():
                print("FAIL: Events are not in chronological order.")
            else:
                print("PASS: Events can be arranged chronologically.")

        # 4. Check exact duplicate rows
        duplicates = df.duplicated().sum()
        print(f"\nExact duplicate rows: {duplicates}")

        if duplicates == 0:
            print("PASS: No exact duplicate rows.")
        else:
            print("WARNING: Duplicate rows found; review them.")

print("\nValidation completed.")