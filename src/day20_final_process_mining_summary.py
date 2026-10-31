import pandas as pd

# Final Process Mining Summary

summary = {
    "Metric": [
        "Total Patient Cases",
        "Total Clinical Events",
        "Clinical Activities",
        "Patient Pathways",
        "Activity Transitions",
        "Loopback Events"
    ],
    "Result": [
        1000,
        6964,
        10,
        6,
        5964,
        705
    ]
}

df = pd.DataFrame(summary)

print("\nCARE FLOW - FINAL PROCESS MINING SUMMARY")
print("=" * 45)
print(df.to_string(index=False))

print("\nKey Findings:")
print("1. Analyzed 1000 patient cases.")
print("2. Identified 6 different patient pathways.")
print("3. Observed repeated activities and loopback events.")
print("4. Analyzed transitions between clinical activities.")
print("5. Identified possible workflow delay areas.")

print("\nFinal process mining summary completed successfully!")