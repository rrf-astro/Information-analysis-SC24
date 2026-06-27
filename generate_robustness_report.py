# =============================================================================
# Generate robustness_analysis.md  (repository hygiene — consolidation step)
#
# Reads the eight robustness CSVs and emits a single human-readable report.
# Every numeric value in the report is read directly from the source CSV via
# pandas; no number is hand-typed, so the report cannot diverge from its source.
#
# Self-contained: depends only on pandas. Run from the directory holding the
# CSVs (or set DATA_DIR). Writes robustness_analysis.md next to them.
# This script is an authoring tool; it is NOT part of the reproducible pipeline
# and is NOT shipped in the public repository.
# =============================================================================

import pandas as pd
from pathlib import Path

DATA_DIR = Path(".")
OUT = DATA_DIR / "robustness_analysis.md"


# Display-only label rewrites. These touch presentation strings, never numbers,
# and never the source CSVs or the notebook cells (jargon in cells is handled in
# a later phase). Phase-internal tags are removed; scientific terms are kept.
LABEL_FIXES = {
    "plug-in n=10 (current)": "plug-in n=10",  # drop phase tag "(current)"
    "AAFT_by_branch": "AAFT",                   # drop internal "_by_branch"
}


# Columns that are counts or identifiers: rendered as integers, never .4f.
INT_COLUMNS = {"n_windows", "mw_U", "MW_U", "block", "n_boot", "seed"}

# Columns whose values are p-values: scientific notation so tiny values survive.
P_COLUMNS = {"p_naive", "p_intra_plateau", "p_null_le_obs", "p", "p_value"}


def _fmt_cell(col, val):
    # p-value columns: scientific notation so tiny values survive
    if col in P_COLUMNS:
        try:
            return f"{float(val):.3e}"
        except (TypeError, ValueError):
            return str(val)
    # count / identifier columns: integer display
    if col in INT_COLUMNS:
        try:
            return str(int(round(float(val))))
        except (TypeError, ValueError):
            return str(val)
    # label rewrites (display-only, never touches source or numbers)
    if isinstance(val, str):
        return LABEL_FIXES.get(val, val)
    # metric floats/ints: fixed 4-decimal display (keeps 1.0000 aligned)
    if isinstance(val, (int, float)):
        return f"{float(val):.4f}"
    return val


def tbl(df: pd.DataFrame) -> str:
    """Render as markdown. Every cell is pre-formatted to its final display
    string and the column is cast to object, so tabulate cannot re-parse and
    flatten p-values or drop trailing zeros."""
    disp = df.copy()
    for col in disp.columns:
        disp[col] = pd.Series([_fmt_cell(col, v) for v in disp[col]], dtype=object)
    return disp.to_markdown(index=False, disable_numparse=True)


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


# ---- load all eight sources -------------------------------------------------
mi_est    = load("mi_estimators.csv")
bboot     = load("block_bootstrap_pvalues.csv")
chref     = load("ch_reference_signals.csv")
extphase  = load("external_phase_tests.csv")
lzc       = load("lzc_lognorm.csv")
closure   = load("closure_gap_null.csv")
pesat     = load("pe_saturation.csv")
extrarefs = load("extra_refs.csv")

# convenience scalars pulled straight from the frames (no literals)
kr3 = mi_est.loc[mi_est.estimator == "Kraskov k=3"].iloc[0]
kr5 = mi_est.loc[mi_est.estimator == "Kraskov k=5"].iloc[0]
plug = mi_est.loc[mi_est.estimator.str.startswith("plug-in n=10")].iloc[0]

c = closure.iloc[0]
closure_method_disp = LABEL_FIXES.get(c.null_method, c.null_method)
ps = pesat.iloc[0]
rMIH  = extrarefs.loc[extrarefs.pair == "r(MI,H_TSA)"].iloc[0]
rMILZ = extrarefs.loc[extrarefs.pair == "r(MI,LZC_TSA)"].iloc[0]
pear  = bboot.loc[bboot.test == "Pearson H-LZC"].iloc[0]
cmax  = chref.loc[chref.signal == "SC24_C_max"].iloc[0]

# ---- assemble report --------------------------------------------------------
parts = []

parts.append(
"""# Robustness Analysis

Supporting robustness checks for the information-theoretic analysis of Total
Sunspot Area (TSA) and Photospheric Sunspot Index (PSI) over Solar Cycle 24.
Each section reports one diagnostic together with the full table of its
underlying values. All figures are read directly from the analysis outputs;
this document is generated, not transcribed.
"""
)

# 1 -- MI estimator robustness
parts.append(
f"""## 1. Mutual-information estimator robustness

Peak-to-trough modulation of the windowed mutual information I(TSA;PSI) under
six estimators. The plug-in estimators carry a positive discretisation bias
that inflates the modulation ratio at fine binning; the bias-corrected Kraskov
k-NN estimators give the physically reported magnitude of the modulation
(approximately {min(kr3.modulation_ratio, kr5.modulation_ratio):.2f}x and above).
The plug-in n=10 ratio of {plug.modulation_ratio:.2f}x reflects estimator bias,
not a larger physical effect, and is not cited as a physical magnitude.

{tbl(mi_est)}
"""
)

# 2 -- block-bootstrap significance
parts.append(
f"""## 2. Block-bootstrap significance

Moving-block bootstrap confidence intervals and naive p-values for the principal
comparative and correlation statistics. The Mann-Whitney rank-biserial effects
for H, LZC and MI are robust (confidence intervals exclude zero); the
permutation-entropy contrast (PE_TSA) is not robust, consistent with PE being
flat across the high-activity plateau. The H-LZC Pearson correlation is
r = {pear.value:.4f}.

{tbl(bboot)}
"""
)

# 3 -- reference-signal calibration
parts.append(
f"""## 3. Reference-signal calibration

Normalised entropy and LMC statistical complexity for synthetic control signals
and for the SC24 complexity extrema, locating the observed values against
white-noise, 1/f, periodic and phase-shuffled benchmarks. The SC24 complexity
maximum reaches C_LMC = {cmax.C_LMC:.4f}.

{tbl(chref)}
"""
)

# 4 -- external-phase split
parts.append(
f"""## 4. External-phase split (peak-split robustness)

Repetition of the Mann-Whitney phase contrasts using an externally defined
ascending/descending split rather than the activity-peak split. The ordering of
the metrics is preserved: the MI and entropy contrasts remain large, while the
PE contrast remains weak.

{tbl(extphase)}
"""
)

# 5 -- LZC log-normalisation
parts.append(
f"""## 5. Lempel-Ziv complexity normalisation

Lempel-Ziv complexity reported as the raw c/n ratio and as the log-normalised
LZC, for TSA and PSI at daily, monthly and annual scales.

{tbl(lzc)}
"""
)

# 6 -- closure-gap null model
parts.append(
f"""## 6. Closure-gap null model

The observed closure gap between cycle start and end is {c.observed_gap_pct:.1f}%,
below the {closure_method_disp} surrogate-null median of {c.null_median:.1f}%
(95% CI [{c.null_ci_lo:.1f}%, {c.null_ci_hi:.1f}%]); p = {c.p_null_le_obs:.4f},
i.e. descriptive rather than statistically significant. The start-of-cycle
anchors are r(MI) = {c.r_start_MI:.4f}, r(LZC) = {c.r_start_LZC:.4f}; the
end-of-cycle anchors are r(MI) = {c.r_end_MI:.4f}, r(LZC) = {c.r_end_LZC:.4f}.

{tbl(closure)}
"""
)

# 7 -- PE saturation / plateau
parts.append(
f"""## 7. Permutation-entropy saturation (plateau)

Permutation entropy across the {ps.scope.replace('_', ' to ')} high-activity
window (n = {int(ps.n_windows)} windows). PE is flat within the plateau: the
intra-plateau Mann-Whitney test gives p = {ps.p_intra_plateau:.4f}, supporting
the decision to treat PE as weakly modulated over the full cycle rather than
phase-discriminating within the active plateau.

{tbl(pesat)}
"""
)

# 8 -- r(MI,.) provenance
parts.append(
f"""## 8. Correlation provenance: r(MI, .)

Moving-block bootstrap correlations of the windowed mutual information against
windowed entropy and Lempel-Ziv complexity, with method parameters. The MI-H
correlation is r = {rMIH.r:.4f}; the MI-LZC correlation is r = {rMILZ.r:.4f}.

{tbl(extrarefs)}
"""
)

OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT}  ({OUT.stat().st_size} bytes)")
