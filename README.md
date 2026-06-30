# Informational analysis of TSA and PSI in Solar Cycle 24

Information-theoretic characterisation of solar activity over Solar Cycle 24
(2008–2019), using the Total Sunspot Area (TSA) and the Photospheric Sunspot
Index (PSI) from the Mandal (2020) catalogue. The analysis applies Shannon
entropy (H), Lempel–Ziv complexity (LZC), mutual information (I), permutation
entropy (PE), López–Mancini–Calbet statistical complexity (C_LMC) and
Jensen–Shannon divergence (D_JS) to daily, monthly and annual series, and
tracks their evolution through the cycle with a sliding window.

This repository contains the analysis notebook, the raw catalogue, the figures
of the manuscript, and the full set of result tables needed to reproduce every
reported number.

## Reproducing the analysis

```bash
pip install -r requirements.txt
jupyter notebook SC24_info_analysis.ipynb   # Run All
```

The notebook reads the two catalogue files (`Mandall2020_catalog1.tsv`,
`Mandall2020_catalog2.tsv`) included here. If those files are absent it will
attempt to query the Mandal (2020) catalogue from CDS VizieR
(`J/A+A/640/A78`) via `astroquery`. A full run regenerates every figure, every
CSV in the root, the `diagnostics/` folder, and the three diagnostic reports
inside it.

After running the notebook, the robustness report can be
regenerated from the result CSVs with:

```bash
python generate_robustness_report.py    # writes robustness_analysis.md
```

## Repository layout

### Notebook and scripts
- `SC24_info_analysis.ipynb` — the complete analysis, from catalogue ingestion
  to every figure and table.
- `generate_robustness_report.py` — assembles `robustness_analysis.md` from the
  robustness CSVs (no hand-typed numbers; all values read from the files).

### Data
- `Mandall2020_catalog1.tsv`, `Mandall2020_catalog2.tsv` — the Mandal (2020)
  sunspot-area/index catalogue used as input.

### Figures
`1.png`–`9.png` are the manuscript figures; `9_CH_3D_supp.png` is the
supplementary 3-D complexity–entropy trajectory.

### Result tables (root)
These CSVs hold every value reported in the manuscript and are produced directly
by the notebook.

| File | Content |
|---|---|
| `table_II.csv` | Static H, PE, LZC, I at daily/monthly/annual scales (Table II). |
| `sliding_window_metrics.csv` | Full 26-month sliding-window series for all metrics with confidence bands. |
| `summary_statistics.csv` | Descriptive reference statistics. |
| `hysteresis_lag_sensitivity.csv` | Hysteresis lag across the window × bin grid. |
| `monthly_coverage.csv` | Monthly observational coverage. |
| `mi_estimators.csv` | Mutual-information modulation under six estimators. |
| `block_bootstrap_pvalues.csv` | Block-bootstrap effect sizes and confidence intervals. |
| `ch_reference_signals.csv` | Complexity–entropy calibration signals. |
| `external_phase_tests.csv` | Phase contrasts under an externally defined (SILSO) split. |
| `lzc_lognorm.csv` | Lempel–Ziv complexity, raw and log-normalised. |
| `closure_gap_null.csv` | Cycle closure gap against an AAFT surrogate null. |
| `pe_saturation.csv` | Permutation-entropy behaviour within the activity plateau. |
| `extra_refs.csv` | Bootstrap correlations of mutual information with H and LZC. |

`robustness_analysis.md` is a generated, human-readable digest of the eight
robustness tables above.

### `diagnostics/`
Internal diagnostic outputs produced by the notebook. They are **not** cited in
the manuscript and are kept only for inspection and method transparency:

- `table_min_max.csv` — windowed minimum/maximum comparison (see note below).
- `mi_estimator_series.csv` — per-window mutual-information series across estimators.
- `pe_dual_compare.csv`, `pe_triple_compare.csv` — permutation-entropy input
  comparisons (continuous vs. symbolic vs. jittered).
- `robustness_summary.md`, `supplementary_robustness.md`, `integrity_report.md` —
  run logs and an integrity gate report generated during execution.

## A note on permutation entropy

Permutation entropy is evaluated with three distinct tests that should not be
conflated: (i) an *intra-plateau* test over 2011–2015, which finds PE flat
(Mann–Whitney p ≈ 0.61); (ii) a *full-cycle* rank-biserial test, which is weak
and not robust (≈ 0.04, p ≈ 0.81); and (iii) an *external/SILSO phase-split*
test, which shows a weak but preserved modulation (rank-biserial ≈ 0.385,
p ≈ 0.007). The reported interpretation — PE saturates within the high-activity
plateau and modulates only weakly over the full cycle — follows from all three
together.

## Reproducibility note

`requirements.txt` pins the versions used to produce the frozen results. `scipy`
is pinned deliberately: its Mann–Whitney U routine has changed across releases,
which can shift the diagnostic `table_min_max.csv` (MW_U by a few units) without
altering any reported scientific conclusion.

## Data source

Sunspot data: Mandal, S. (2020), via CDS VizieR catalogue `J/A+A/640/A78`.
Please cite the original catalogue when using these data.

## License

The contents of this repository are released under the
**Creative Commons Attribution 4.0 International (CC BY 4.0)** license.
See `LICENSE`. You are free to share and adapt the material for any purpose,
provided appropriate credit is given.

## Citation

The associated manuscript, *Informational analysis of TSA and PSI in Solar
Cycle 24*, is in preparation / under submission. A citation entry with DOI will
be added here on acceptance. In the meantime, please cite this repository and
its author (Rafael R. Ferreira) when using the code or derived tables.
