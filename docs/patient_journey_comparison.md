# Day 18: Patient Journey Comparison Analysis

## Objective
Compare complete patient pathways by frequency and journey duration.

## Dataset Summary
- Patients analyzed: 1000
- Unique pathways: 6
- Total events: 6964

## Pathway Comparison

| activity_sequence                                                                                                                                                              |   patient_count |   average_journey_duration_minutes |   minimum_journey_duration_minutes |   maximum_journey_duration_minutes |   percentage_of_patients |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|-------------------------:|
| Registration -> Triage -> Doctor Assessment -> Discharge                                                                                                                       |             267 |                              58.55 |                                 12 |                                107 |                     26.7 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Documentation Review -> Discharge                                                                  |             216 |                             102.34 |                                 52 |                                158 |                     21.6 |
| Registration -> Triage -> Doctor Assessment -> Lab Collection -> Lab Result -> Discharge                                                                                       |             149 |                             102.92 |                                 44 |                                157 |                     14.9 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Triage -> Documentation Review -> Doctor Reassessment -> Discharge                                 |             146 |                             132.82 |                                 73 |                                192 |                     14.6 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Documentation Review -> Lab Collection -> Lab Result -> Discharge                                  |             133 |                             146.56 |                                 84 |                                207 |                     13.3 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Triage -> Documentation Review -> Doctor Reassessment -> Lab Collection -> Lab Result -> Discharge |              89 |                             174.57 |                                120 |                                234 |                      8.9 |

## Interpretation
- Patient count indicates how frequently each pathway occurs.
- Average journey duration measures elapsed time from first to last recorded event.
- Minimum and maximum show the observed duration range.
- Longer elapsed duration alone does not prove a clinical bottleneck.

## Output
- `data\processed\patient_journey_comparison_summary.csv`