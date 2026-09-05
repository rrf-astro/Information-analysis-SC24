#!/usr/bin/env python3
"""Fetch Mandal (2020) TSA (Areac) and PSI from VizieR J/A+A/640/A78 and export
daily (max-abs normalised) and monthly-mean CSVs for the contribution notebook.

Run on a machine with internet access (e.g. your Mac's terminal), from anywhere:
    python3 fetch_tsa_psi.py

Writes, next to this script:
    data/sc24_daily.csv     (Date, TSA, PSI  — daily, max-abs normalised)
    data/sc24_monthly.csv   (Date, TSA, PSI  — monthly mean)

It does NOT need the rest of Rafael's notebook; it only reproduces its data query.
Requires astroquery (the same package the notebook already uses).
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd
from astroquery.vizier import Vizier

CAT = 'J/A+A/640/A78'
OUT = Path(__file__).resolve().parent / 'data'
OUT.mkdir(parents=True, exist_ok=True)
SERVERS = ['vizier.cds.unistra.fr', 'vizier.cfa.harvard.edu',
           'vizier.china-vo.org', 'vizier.nao.ac.jp', 'vizier.hia.nrc.ca']

def fetch():
    last = None
    for srv in SERVERS:
        for k in range(3):
            try:
                v = Vizier(columns=['Obs.date', 'Areac', 'PSI']); v.ROW_LIMIT = -1
                v.VIZIER_SERVER = srv
                res = v.get_catalogs(CAT)
                if len(res) == 0:
                    raise RuntimeError('empty TableList (server returned no tables)')
                t = res[0].to_pandas()
                print(f'[ok] {srv}: {len(t)} rows | columns = {list(t.columns)}')
                return t
            except Exception as e:
                last = e; print(f'[retry] {srv} #{k+1}: {e}'); time.sleep(4)
    sys.exit(f'\nAll servers failed (last error: {last}).\n'
             'VizieR is likely momentarily unavailable — wait a minute and re-run.')

t = fetch()
low = {c.lower(): c for c in t.columns}
def pick(*keys):
    for key in keys:
        for lc, orig in low.items():
            if key in lc: return orig
    return None
dcol, acol, pcol = pick('date'), pick('areac', 'area', 'tsa'), pick('psi')
if None in (dcol, acol, pcol):
    sys.exit(f'could not map columns from {list(t.columns)} '
             f'(date={dcol}, TSA={acol}, PSI={pcol})')

df = t[[dcol, acol, pcol]].copy(); df.columns = ['Date', 'TSA', 'PSI']
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna().set_index('Date').sort_index()
df = df[(df.index >= '2008-12-01') & (df.index <= '2019-10-31')]

daily = df / df.abs().max()                       # max-abs normalisation (matches CELL 3)
daily.to_csv(OUT / 'sc24_daily.csv', index_label='Date')
monthly = df.resample('ME').mean()
monthly.to_csv(OUT / 'sc24_monthly.csv', index_label='Date')

print(f'\nwrote {OUT/"sc24_daily.csv"}   ({len(daily)} days,  {daily.index.min().date()} -> {daily.index.max().date()})')
print(f'wrote {OUT/"sc24_monthly.csv"}  ({len(monthly)} months)')
print('done — tell Claude the files are in data/ and it will finish the two extras.')
