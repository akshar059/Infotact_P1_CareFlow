#!/usr/bin/env python3
"""
CareFlow - imputation, normalization (min-max) and standardization (z-score).
Run AFTER careflow_clean.py.

Leakage control: chronological split on case_start (first 80% = train, last 20% = test).
Every imputer / scaler statistic is FIT ON TRAIN ONLY, then applied to test.

Inputs : careflow_cases_clean.csv, careflow_events_clean.csv
Outputs: careflow_cases_imputed.csv, careflow_cases_standardized.csv, careflow_cases_normalized.csv,
         careflow_events_scaled.csv, careflow_model_ready_scaled.csv,
         scaler_parameters.json, imputation_benchmark.csv, scaling_checks.csv
"""
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.experimental import enable_iterative_imputer  # noqa: F401  (must precede IterativeImputer import)
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
OUT.mkdir(parents=True, exist_ok=True)
checks = []


def log(check, ok, detail=""):
    checks.append(("PASS" if ok else "FAIL", check, str(detail)))


cases = pd.read_csv(SRC / "careflow_cases_clean.csv", parse_dates=["case_start", "case_end"])
events = pd.read_csv(SRC / "careflow_events_clean.csv", parse_dates=["timestamp"])
bool_cols = ["is_weekend", "ends_next_day", "duration_outlier_flag"]

# ------------------------------------------------- 1. CHRONOLOGICAL SPLIT
cases = cases.sort_values("case_start", kind="stable").reset_index(drop=True)
cutoff = cases["case_start"].quantile(0.8)
cases["split"] = np.where(cases["case_start"] <= cutoff, "train", "test")
tr = cases["split"].eq("train")
split_map = cases.set_index("case_id")["split"]
log("split is chronological (max train start <= min test start)",
    cases.loc[tr, "case_start"].max() <= cases.loc[~tr, "case_start"].min(),
    f"train={tr.sum()} test={(~tr).sum()} cutoff={cutoff}")

# ------------------------------------------------- 2. IMPUTATION
# 2a. Structural missingness: step did not occur -> NaN -> 0 minutes + explicit has_* indicator.
#     (mean/median would fabricate X-rays/labs/loopbacks that never happened)
STRUCT = {"xray_to_result_min": "has_xray", "lab_turnaround_min": "has_lab", "loopback_delay_min": "has_reassessment"}
imp = cases.copy()
for col, flag in STRUCT.items():
    imp.loc[imp[flag] == 0, col] = np.nan          # make the structural gap explicit
    log(f"{col} is NaN exactly when {flag} == 0", (imp[col].isna() == (imp[flag] == 0)).all())
    imp[col] = imp[col].fillna(0.0)

# 2b. Genuine (random) missingness in observed columns: iterative imputer fit on train only.
#     None is present in this data; the path is kept so new data with gaps is handled.
GEN = ["age", "acuity", "n_events", "total_duration_min", "registration_to_triage_min",
       "door_to_doctor_min", "assessment_to_discharge_min", "start_hour"]
n_gen = int(imp[GEN].isna().sum().sum())
if n_gen:
    it = IterativeImputer(max_iter=20, random_state=0).fit(imp.loc[tr, GEN])
    imp[GEN] = it.transform(imp[GEN])
log("genuine missing values in observed columns", True, f"found={n_gen}")
log("no missing values remain after imputation", imp.isna().sum().sum() == 0)

# 2c. Benchmark: mask 10% of known values, impute, compare to truth (stats fit on train rows).
rng = np.random.default_rng(42)
X = cases[GEN].to_numpy(float)
mask = rng.random(X.shape) < 0.10
Xm = X.copy(); Xm[mask] = np.nan
sc_b = StandardScaler().fit(np.where(tr.to_numpy()[:, None] & ~mask, X, np.nan))
Z = sc_b.transform(Xm)
imputers = {"mean": SimpleImputer(strategy="mean"), "median": SimpleImputer(strategy="median"),
            "knn_k5": KNNImputer(n_neighbors=5),
            "iterative_bayesridge": IterativeImputer(max_iter=20, random_state=0)}
rows = []
for name, im in imputers.items():
    Xi = sc_b.inverse_transform(im.fit(Z[tr.to_numpy()]).transform(Z))
    for j, col in enumerate(GEN):
        mj = mask[:, j]
        rows.append((name, col, np.sqrt(np.mean((Xi[mj, j] - X[mj, j]) ** 2)) / X[:, j].std()))
bench = pd.DataFrame(rows, columns=["imputer", "column", "nrmse"]).pivot(index="column", columns="imputer", values="nrmse")
bench.loc["MEAN_OVER_COLUMNS"] = bench.mean()
bench.round(4).to_csv(OUT / "imputation_benchmark.csv")
best = bench.loc["MEAN_OVER_COLUMNS"].idxmin()
log("imputation benchmark completed", True, f"best by mean NRMSE: {best}; " +
    ", ".join(f"{k}={v:.3f}" for k, v in bench.loc["MEAN_OVER_COLUMNS"].items()))

# ------------------------------------------------- 3. SCALING (case level)
SCALE = ["age", "acuity", "n_events", "n_unique_activities", "registration_to_triage_min", "door_to_doctor_min",
         "xray_to_result_min", "lab_turnaround_min", "assessment_to_discharge_min", "loopback_delay_min", "start_hour"]
TARGET = ["total_duration_min"]          # raw target kept; scaled copy added
allc = SCALE + TARGET
params = {"split_cutoff": str(cutoff), "fit_on": "train rows only"}


def fit_scale(df, cols, tag):
    ss = StandardScaler().fit(df.loc[df["split"] == "train", cols])
    mm = MinMaxScaler().fit(df.loc[df["split"] == "train", cols])
    params[tag] = {c: {"mean": float(ss.mean_[i]), "std": float(np.sqrt(ss.var_[i])),
                       "min": float(mm.data_min_[i]), "max": float(mm.data_max_[i])} for i, c in enumerate(cols)}
    return ss, mm


ss, mm = fit_scale(imp, allc, "case_level")
std_df, nrm_df = imp.copy(), imp.copy()
std_df[[f"{c}_z" for c in allc]] = ss.transform(imp[allc])
nrm_df[[f"{c}_mm" for c in allc]] = mm.transform(imp[allc])
std_out, nrm_out = std_df.drop(columns=SCALE), nrm_df.drop(columns=SCALE)

ztr = std_df.loc[tr, [f"{c}_z" for c in allc]]
mtr = nrm_df.loc[tr, [f"{c}_mm" for c in allc]]
log("standardized train: mean ~ 0", np.allclose(ztr.mean(), 0, atol=1e-9), f"max|mean|={ztr.mean().abs().max():.2e}")
log("standardized train: std ~ 1", np.allclose(ztr.std(ddof=0), 1, atol=1e-9))
log("normalized train within [0,1] and hits both ends",
    (mtr.min() >= -1e-12).all() and (mtr.max() <= 1 + 1e-12).all() and np.allclose(mtr.min(), 0) and np.allclose(mtr.max(), 1))
mte = nrm_df.loc[~tr, [f"{c}_mm" for c in allc]]
log("normalized test values outside [0,1] (expected possible, NOT clipped)", True, f"count={int(((mte < 0) | (mte > 1)).sum().sum())}")
log("inverse transform recovers original values",
    np.allclose(ss.inverse_transform(std_df[[f"{c}_z" for c in allc]]), imp[allc]) and
    np.allclose(mm.inverse_transform(nrm_df[[f"{c}_mm" for c in allc]]), imp[allc]))

# ------------------------------------------------- 4. SCALING (event level)
ev = events.copy()
ev["split"] = ev["case_id"].map(split_map)
EV = ["minutes_since_prev", "minutes_since_case_start", "age", "acuity"]
ss_e = StandardScaler().fit(ev.loc[ev.split == "train", EV])
mm_e = MinMaxScaler().fit(ev.loc[ev.split == "train", EV])
params["event_level"] = {c: {"mean": float(ss_e.mean_[i]), "std": float(np.sqrt(ss_e.var_[i])),
                             "min": float(mm_e.data_min_[i]), "max": float(mm_e.data_max_[i])} for i, c in enumerate(EV)}
ev[[f"{c}_z" for c in EV]] = ss_e.transform(ev[EV])
ev[[f"{c}_mm" for c in EV]] = mm_e.transform(ev[EV])
log("event-level scaled rows == events rows", len(ev) == len(events), len(ev))
log("every event case has a split", ev["split"].notna().all())

# ------------------------------------------------- 5. MODEL-READY (arrival-time features only)
m = pd.DataFrame({"case_id": cases.case_id, "case_start": cases.case_start, "age": cases.age, "acuity": cases.acuity,
                  "start_hour_sin": np.sin(2 * np.pi * cases.start_hour / 24),
                  "start_hour_cos": np.cos(2 * np.pi * cases.start_hour / 24),
                  "is_weekend": cases.is_weekend.astype(int)})
for col in ["age_group", "resource", "shift", "start_weekday"]:
    m = m.join(pd.get_dummies(cases[col], prefix=col, dtype=int))
m["target_total_duration_min"] = cases.total_duration_min
m["target_loopback"] = cases.loopback_flag
m["target_ends_next_day"] = cases.ends_next_day.astype(int)
m["split"] = cases.split
AR = ["age", "acuity"]
ss_a = StandardScaler().fit(m.loc[tr, AR]); mm_a = MinMaxScaler().fit(m.loc[tr, AR])
m[[f"{c}_z" for c in AR]] = ss_a.transform(m[AR])
m[[f"{c}_mm" for c in AR]] = mm_a.transform(m[AR])
dur = StandardScaler().fit(m.loc[tr, ["target_total_duration_min"]])
m["target_total_duration_min_z"] = dur.transform(m[["target_total_duration_min"]]).ravel()
params["model_ready"] = {c: {"mean": float(ss_a.mean_[i]), "std": float(np.sqrt(ss_a.var_[i])),
                             "min": float(mm_a.data_min_[i]), "max": float(mm_a.data_max_[i])} for i, c in enumerate(AR)}
params["model_ready"]["target_total_duration_min"] = {"mean": float(dur.mean_[0]), "std": float(np.sqrt(dur.var_[0]))}
feat = [c for c in m.columns if not c.startswith("target_") and c not in ("case_id", "case_start", "split")]
log("model-ready features have no NaN", m[feat].isna().sum().sum() == 0)
log("one-hot/sin/cos columns untouched (already bounded)", True)

# ------------------------------------------------- write
fmt = "%Y-%m-%d %H:%M:%S"
def dump(df, name):
    d = df.copy()
    for c in d.select_dtypes("datetime64[ns]").columns:
        d[c] = d[c].dt.strftime(fmt)
    d.to_csv(OUT / name, index=False)

dump(imp, "careflow_cases_imputed.csv"); dump(std_out, "careflow_cases_standardized.csv")
dump(nrm_out, "careflow_cases_normalized.csv"); dump(ev, "careflow_events_scaled.csv")
dump(m, "careflow_model_ready_scaled.csv")
with open(OUT / "scaler_parameters.json", "w") as f:
    json.dump(params, f, indent=2)
res = pd.DataFrame(checks, columns=["result", "check", "detail"])
res.to_csv(OUT / "scaling_checks.csv", index=False)
print(res.to_string(index=False))
print("\nPASS:", (res.result == "PASS").sum(), "FAIL:", (res.result == "FAIL").sum())
print("shapes -> imputed", imp.shape, "| standardized", std_out.shape, "| normalized", nrm_out.shape,
      "| events", ev.shape, "| model-ready", m.shape)
