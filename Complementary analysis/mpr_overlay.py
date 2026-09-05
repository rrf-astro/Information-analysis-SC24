# Overlay SC24 on the MPR plane once the raw daily series is available.
# Expects a CSV with columns: Date, TSA, PSI (daily, as used for Table II).
# Drop the file in this folder as 'sc24_daily.csv' and run:  python3 mpr_overlay.py
import numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, ordpy, sys, os

CSV = sys.argv[1] if len(sys.argv)>1 else 'sc24_daily.csv'
if not os.path.exists(CSV):
    sys.exit(f"Provide {CSV} (Date,TSA,PSI daily) — export df_normalizado/df_diario from CELL 3.")
df = pd.read_csv(CSV)
for DX in (4,5,6):
    hT,cT = ordpy.complexity_entropy(df['TSA'].values, dx=DX)
    hP,cP = ordpy.complexity_entropy(df['PSI'].values, dx=DX)
    print(f"dx={DX}:  TSA H={hT:.4f} C={cT:.4f}   PSI H={hP:.4f} C={cP:.4f}")
# Distance of SC24 from the white-noise corner and to the max-complexity envelope,
# reported per dx, is the ordinal-framework counterpart of ch_reference_signals.csv.
