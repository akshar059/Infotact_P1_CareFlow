# Day 19: Process Mining Insights and Findings Report

## 1. Project Overview
This report consolidates the process mining findings from the CareFlow clinical workflow dataset.

## 2. Dataset Overview
- Total patients analyzed: 1,000
- Total recorded events: 6,964
- Activity types: 10
- Recorded transitions: 5,964

## 3. Activity Frequency Findings
| activity_name        |   event_count |   unique_cases |   percentage_of_events |   percentage_of_cases |   repeat_event_count |
|:---------------------|--------------:|---------------:|-----------------------:|----------------------:|---------------------:|
| Triage               |          1235 |           1000 |                  17.73 |                 100   |                  235 |
| Discharge            |          1000 |           1000 |                  14.36 |                 100   |                    0 |
| Doctor Assessment    |          1000 |           1000 |                  14.36 |                 100   |                    0 |
| Registration         |          1000 |           1000 |                  14.36 |                 100   |                    0 |
| Documentation Review |           584 |            584 |                   8.39 |                  58.4 |                    0 |
| Radiology Result     |           584 |            584 |                   8.39 |                  58.4 |                    0 |
| X-Ray                |           584 |            584 |                   8.39 |                  58.4 |                    0 |
| Lab Collection       |           371 |            371 |                   5.33 |                  37.1 |                    0 |
| Lab Result           |           371 |            371 |                   5.33 |                  37.1 |                    0 |
| Doctor Reassessment  |           235 |            235 |                   3.37 |                  23.5 |                    0 |

## 4. Patient Pathway Findings
| pathway                                                                                                                                                                        |   case_count |   percentage |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------:|-------------:|
| Registration -> Triage -> Doctor Assessment -> Discharge                                                                                                                       |          267 |         26.7 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Documentation Review -> Discharge                                                                  |          216 |         21.6 |
| Registration -> Triage -> Doctor Assessment -> Lab Collection -> Lab Result -> Discharge                                                                                       |          149 |         14.9 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Triage -> Documentation Review -> Doctor Reassessment -> Discharge                                 |          146 |         14.6 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Documentation Review -> Lab Collection -> Lab Result -> Discharge                                  |          133 |         13.3 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Triage -> Documentation Review -> Doctor Reassessment -> Lab Collection -> Lab Result -> Discharge |           89 |          8.9 |

## 5. Loopback Findings
| activity_name        |   loopback_event_count |
|:---------------------|-----------------------:|
| Doctor Reassessment  |                    235 |
| Documentation Review |                    235 |
| Triage               |                    235 |

## 6. Waiting Time Findings
| from_activity        | to_activity          |   transition_count |   average_minutes |   median_minutes |   maximum_minutes |
|:---------------------|:---------------------|-------------------:|------------------:|-----------------:|------------------:|
| Lab Collection       | Lab Result           |                371 |             32.56 |               32 |                50 |
| Triage               | Doctor Assessment    |               1000 |             30.74 |               29 |                60 |
| X-Ray                | Radiology Result     |                584 |             22.42 |               22 |                35 |
| Documentation Review | Discharge            |                216 |             15.5  |               16 |                25 |
| Doctor Reassessment  | Discharge            |                146 |             15.37 |               16 |                25 |
| Doctor Assessment    | X-Ray                |                584 |             15.09 |               15 |                25 |
| Lab Result           | Discharge            |                371 |             14.87 |               14 |                25 |
| Triage               | Documentation Review |                235 |             14.8  |               15 |                25 |
| Doctor Assessment    | Discharge            |                267 |             14.79 |               15 |                25 |
| Registration         | Triage               |               1000 |             12.62 |               12 |                25 |

## 7. Patient Journey Comparison
| activity_sequence                                                                                                                                                              |   patient_count |   average_journey_duration_minutes |   minimum_journey_duration_minutes |   maximum_journey_duration_minutes |   percentage_of_patients |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|-------------------------:|
| Registration -> Triage -> Doctor Assessment -> Discharge                                                                                                                       |             267 |                              58.55 |                                 12 |                                107 |                     26.7 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Documentation Review -> Discharge                                                                  |             216 |                             102.34 |                                 52 |                                158 |                     21.6 |
| Registration -> Triage -> Doctor Assessment -> Lab Collection -> Lab Result -> Discharge                                                                                       |             149 |                             102.92 |                                 44 |                                157 |                     14.9 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Triage -> Documentation Review -> Doctor Reassessment -> Discharge                                 |             146 |                             132.82 |                                 73 |                                192 |                     14.6 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Documentation Review -> Lab Collection -> Lab Result -> Discharge                                  |             133 |                             146.56 |                                 84 |                                207 |                     13.3 |
| Registration -> Triage -> Doctor Assessment -> X-Ray -> Radiology Result -> Triage -> Documentation Review -> Doctor Reassessment -> Lab Collection -> Lab Result -> Discharge |              89 |                             174.57 |                                120 |                                234 |                      8.9 |

## 8. Workflow Performance Summary
|   rank_by_average_elapsed | from_activity        | to_activity          |   transition_count |   average_elapsed_minutes |   median_elapsed_minutes |   maximum_elapsed_minutes |   frequency_rank |
|--------------------------:|:---------------------|:---------------------|-------------------:|--------------------------:|-------------------------:|--------------------------:|-----------------:|
|                         1 | Lab Collection       | Lab Result           |                371 |                     32.56 |                       32 |                        50 |                3 |
|                         2 | Triage               | Doctor Assessment    |               1000 |                     30.74 |                       29 |                        60 |                1 |
|                         3 | X-Ray                | Radiology Result     |                584 |                     22.42 |                       22 |                        35 |                2 |
|                         4 | Documentation Review | Discharge            |                216 |                     15.5  |                       16 |                        25 |                7 |
|                         5 | Doctor Reassessment  | Discharge            |                146 |                     15.37 |                       16 |                        25 |                9 |
|                         6 | Doctor Assessment    | X-Ray                |                584 |                     15.09 |                       15 |                        25 |                2 |
|                         7 | Lab Result           | Discharge            |                371 |                     14.87 |                       14 |                        25 |                3 |
|                         8 | Triage               | Documentation Review |                235 |                     14.8  |                       15 |                        25 |                6 |
|                         9 | Doctor Assessment    | Discharge            |                267 |                     14.79 |                       15 |                        25 |                5 |
|                        10 | Registration         | Triage               |               1000 |                     12.62 |                       12 |                        25 |                1 |

## 9. Key Observations
- Patient journeys follow multiple activity sequences.
- Direct-discharge and investigation-based pathways have different durations.
- Loopback events indicate repeated workflow activities.
- Waiting-time summaries highlight transitions worth further investigation.
- Elapsed time alone does not establish a clinical bottleneck.

## 10. Improvement Opportunities
- Review repeated triage and reassessment activities.
- Investigate long-duration investigation pathways.
- Review handoffs between investigation and documentation activities.
- Monitor workflow variations to identify opportunities for improvement.

## 11. Conclusion
Process mining helps understand patient workflow patterns, pathway variations, repeated activities, and elapsed journey durations. These findings can support further workflow investigation and improvement.

## 12. Scope and Limitations
- Findings are based on the available recorded event data.
- Elapsed journey duration is not necessarily actual waiting time.
- Improvement opportunities require clinical and operational validation.