# Sierra-Porta contribution — Informational Analysis of TSA and PSI in SC24

Consolidated in **`SC24_SierraPorta_contribution.ipynb`**: three additions, each a
section with Method → calculation → figure (no embedded title) → analysis. The
notebook runs end-to-end from the files in `data/` and the repository's
`sliding_window_metrics.csv`. Requires `ordpy` (`pip install ordpy`) on top of the
pinned environment. All three contributions are complete.

## 1. Confidence interval for the 23-month I–C_LMC lag
The one headline number without an interval. A semi-parametric residual block
bootstrap (perturbs the peaks without scrambling their separation, unlike the retired
case bootstrap) gives **23 months, 95% CI [19, 31]** (raw definition) / [24, 27]
(smoothed vertex), **positive in 100% of replicates**. Frequency-domain phase methods
are shown inapplicable to a single-cycle record, which justifies the peak-to-peak
definition. Figure: `fig_phase_lag.png`.

## 2. Ordinal complexity–entropy (MPR) plane
A bin-free, rescaling-invariant test of the structured-regime claim. All four solar
series land in the structured band: at d=4 TSA=(0.90, 0.10), PSI=(0.82, 0.16),
SSN=(0.82, 0.16), F10.7=(0.86, 0.13), far above every noise reference; at d=6 they
climb to C≈0.26–0.33. The permutation entropy of TSA and PSI reproduces the
manuscript's Table II exactly (0.9045, 0.8231). Figure: `fig_mpr_plane.png`.

## 3. Independent-proxy replication (SSN, F10.7) + catalogue↔proxy couplings
The signatures are solar, not catalogue artefacts. C_LMC(SSN) and C_LMC(F10.7) peak on
the descending branch (2017-02) at ≈0.23–0.24, matching C_LMC(TSA) (2016-09, 0.237);
the three LZC series are nearly identical. Recomputing I(TSA;PSI) on the retrieved data
reproduces the manuscript's 5.3×/1.4× modulation exactly (data validation), and TSA
shares strongly modulated information with the independent proxies — I(TSA;SSN) 4.0×,
I(TSA;F10.7) 2.9× (Kraskov, bias-free). The 23-month hysteresis lag is TSA–PSI-internal
and is not forced onto the proxies. Figure: `fig_proxy_replication.png`.

## Files
- `SC24_SierraPorta_contribution.ipynb` — the consolidated, executed notebook.
- `fig_phase_lag.png`, `fig_mpr_plane.png`, `fig_proxy_replication.png` — title-less figures.
- `data/` — SILSO SSN, Penticton F10.7, the consolidated `proxies_{monthly,daily}.csv`,
  and the retrieved TSA/PSI series `sc24_{daily,monthly}.csv`.
- `fetch_tsa_psi.py` — retrieves TSA/PSI from VizieR (J/A+A/640/A78); run on a networked machine.
- `mpr_overlay.py`, `proxy_replication.py` — standalone helper scripts.
- `lag_estimates.csv` — lag results table.

## Provenance
Raw TSA/PSI retrieved with `fetch_tsa_psi.py` (VizieR J/A+A/640/A78); the retrieval is
confirmed by exact reproduction of the manuscript's Table II permutation entropies and
its I(TSA;PSI) modulation. `seed = 20260531` throughout.
