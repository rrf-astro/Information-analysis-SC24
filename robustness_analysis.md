# Robustness Analysis

Supporting robustness checks for the information-theoretic analysis of Total
Sunspot Area (TSA) and Photospheric Sunspot Index (PSI) over Solar Cycle 24.
Each section reports one diagnostic together with the full table of its
underlying values. All figures are read directly from the analysis outputs;
this document is generated, not transcribed.

## 1. Mutual-information estimator robustness

Peak-to-trough modulation of the windowed mutual information I(TSA;PSI) under
six estimators. The plug-in estimators carry a positive discretisation bias
that inflates the modulation ratio at fine binning; the bias-corrected Kraskov
k-NN estimators give the physically reported magnitude of the modulation
(approximately 1.34x and above).
The plug-in n=10 ratio of 5.30x reflects estimator bias,
not a larger physical effect, and is not cited as a physical magnitude.

| estimator        | MI_max   | MI_min   | modulation_ratio   | mod_ci_lo   | mod_ci_hi   |
|:-----------------|:---------|:---------|:-------------------|:------------|:------------|
| plug-in n=10     | 2.3357   | 0.4410   | 5.2961             | 1.8299      | 5.2961      |
| plug-in n=5+     | 1.9220   | 0.6219   | 3.0905             | 1.5511      | 3.0905      |
| plug-in n=4      | 1.7381   | 0.5530   | 3.1433             | 1.6879      | 3.1433      |
| Miller-Madow n=5 | 2.0053   | 0.6774   | 2.9603             | 1.6309      | 2.9603      |
| Kraskov k=3      | 2.5579   | 1.8326   | 1.3958             | 1.2137      | 1.3958      |
| Kraskov k=5      | 1.9789   | 1.4724   | 1.3440             | 1.2053      | 1.3440      |

## 2. Block-bootstrap significance

Moving-block bootstrap confidence intervals and naive p-values for the principal
comparative and correlation statistics. The Mann-Whitney rank-biserial effects
for H, LZC and MI are robust (confidence intervals exclude zero); the
permutation-entropy contrast (PE_TSA) is not robust, consistent with PE being
flat across the high-activity plateau. The H-LZC Pearson correlation is
r = 0.9656.

| test          | stat          | value   | ci_lo   | ci_hi   | p_naive   | verdict                |
|:--------------|:--------------|:--------|:--------|:--------|:----------|:-----------------------|
| MW H_TSA      | rank_biserial | 0.9810  | 0.9619  | 1.0000  | 1.792e-10 | robust (CI excludes 0) |
| MW LZC_TSA    | rank_biserial | 0.9661  | 0.9323  | 1.0000  | 3.058e-11 | robust (CI excludes 0) |
| MW MI         | rank_biserial | 0.9873  | 0.9746  | 1.0000  | 1.370e-10 | robust (CI excludes 0) |
| MW PE_TSA     | rank_biserial | 0.0381  | -0.2804 | 0.3556  | 8.084e-01 | NOT robust             |
| KS MI         | D             | 0.3962  | 0.2075  | 0.8491  | 4.199e-04 | CI reported            |
| KS LZC_TSA    | D             | 0.3585  | 0.1321  | 0.7736  | 2.022e-03 | CI reported            |
| Pearson H-LZC | r             | 0.9656  | 0.6206  | 0.9800  | 1.136e-62 | CI reported            |

## 3. Reference-signal calibration

Normalised entropy and LMC statistical complexity for synthetic control signals
and for the SC24 complexity extrema, locating the observed values against
white-noise, 1/f, periodic and phase-shuffled benchmarks. The SC24 complexity
maximum reaches C_LMC = 0.2371.

| signal      | H_norm   | C_LMC   |
|:------------|:---------|:--------|
| white_noise | 0.9975   | 0.0020  |
| colored_1/f | 0.8628   | 0.0986  |
| periodic    | 0.9495   | 0.0370  |
| tsa_shuffle | 0.8313   | 0.1135  |
| SC24_C_max  | 0.5894   | 0.2371  |
| SC24_C_min  | 0.8793   | 0.1000  |

## 4. External-phase split (peak-split robustness)

Repetition of the Mann-Whitney phase contrasts using an externally defined
ascending/descending split rather than the activity-peak split. The ordering of
the metrics is preserved: the MI and entropy contrasts remain large, while the
PE contrast remains weak.

| test           | rank_biserial   | ci_lo   | ci_hi   | p_naive   | vs_peak_split   |
|:---------------|:----------------|:--------|:--------|:----------|:----------------|
| MW_ext H_TSA   | 0.9321          | 0.8375  | 1.0000  | 5.731e-11 | preserved       |
| MW_ext LZC_TSA | 0.8571          | 0.7160  | 0.9938  | 3.735e-10 | preserved       |
| MW_ext MI      | 0.9857          | 0.9536  | 1.0000  | 4.311e-12 | preserved       |
| MW_ext PE_TSA  | 0.3848          | 0.0384  | 0.6768  | 6.679e-03 | preserved       |

## 5. Lempel-Ziv complexity normalisation

Lempel-Ziv complexity reported as the raw c/n ratio and as the log-normalised
LZC, for TSA and PSI at daily, monthly and annual scales.

| scale   | series   | LZC_c_over_n   | LZC_lognorm   |
|:--------|:---------|:---------------|:--------------|
| Daily   | TSA      | 0.1254         | 0.4465        |
| Daily   | PSI      | 0.0987         | 0.3516        |
| Monthly | TSA      | 0.3893         | 0.8243        |
| Monthly | PSI      | 0.3664         | 0.7758        |
| Annual  | TSA      | 0.7500         | 0.8094        |
| Annual  | PSI      | 0.7500         | 0.8094        |

## 6. Closure-gap null model

The observed closure gap between cycle start and end is 10.2%,
below the AAFT surrogate-null median of 32.8%
(95% CI [4.0%, 73.2%]); p = 0.1405,
i.e. descriptive rather than statistically significant. The start-of-cycle
anchors are r(MI) = 0.4410, r(LZC) = 0.4231; the
end-of-cycle anchors are r(MI) = 0.6219, r(LZC) = 0.3462.

| observed_gap_pct   | null_median   | null_ci_lo   | null_ci_hi   | p_null_le_obs   | null_method   | r_start_MI   | r_start_LZC   | r_end_MI   | r_end_LZC   |
|:-------------------|:--------------|:-------------|:-------------|:----------------|:--------------|:-------------|:--------------|:-----------|:------------|
| 10.2403            | 32.7546       | 3.9578       | 73.1980      | 1.405e-01       | AAFT          | 0.4410       | 0.4231        | 0.6219     | 0.3462      |

## 7. Permutation-entropy saturation (plateau)

Permutation entropy across the 2011-01 to 2015-12 high-activity
window (n = 60 windows). PE is flat within the plateau: the
intra-plateau Mann-Whitney test gives p = 0.6084, supporting
the decision to treat PE as weakly modulated over the full cycle rather than
phase-discriminating within the active plateau.

| scope           | n_windows   | pe_min   | pe_max   | pe_mean   | pe_std   | split     | mw_U   | p_intra_plateau   | hi_mean   | hi_std   | lo_mean   | lo_std   |
|:----------------|:------------|:---------|:---------|:----------|:---------|:----------|:-------|:------------------|:----------|:---------|:----------|:---------|
| 2011-01_2015-12 | 60          | 0.9215   | 0.9941   | 0.9703    | 0.0196   | MI_median | 485    | 6.084e-01         | 0.9737    | 0.0128   | 0.9670    | 0.0244   |

## 8. Correlation provenance: r(MI, .)

Moving-block bootstrap correlations of the windowed mutual information against
windowed entropy and Lempel-Ziv complexity, with method parameters. The MI-H
correlation is r = 0.9491; the MI-LZC correlation is r = 0.9174.

| pair          | r      | p         | ci_lo   | ci_hi   | method                 | block   | n_boot   | seed     |
|:--------------|:-------|:----------|:--------|:--------|:-----------------------|:--------|:---------|:---------|
| r(MI,H_TSA)   | 0.9491 | 5.538e-54 | 0.8335  | 0.9727  | moving_block_bootstrap | 26      | 2000     | 20260531 |
| r(MI,LZC_TSA) | 0.9174 | 2.098e-43 | 0.5745  | 0.9427  | moving_block_bootstrap | 26      | 2000     | 20260531 |
