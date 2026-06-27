```
============================================================
RELATORIO_NOTEBOOK_LOCAL — SC24_info_analysis.ipynb
Generated automatically by Cell 19
Date/time : 2026-06-26 21:20:11
Python    : 3.12.2
pandas 2.2.2  |  numpy 1.26.4  |  scipy 1.13.1
============================================================

────────────────────────────────────────────────────────────
BLOCK 0 — Catalogue integrity (Cell 2)
────────────────────────────────────────────────────────────
[ OK ]  N observations                            3636  (expected: 3636)
[ OK ]  Last record                               2019-10-02  (expected: 2019-10-02)
[ OK ]  First record                              2008-12-01  (expected: 2008-12-01)

────────────────────────────────────────────────────────────
BLOCK 1 — Table II (Cell 6)
────────────────────────────────────────────────────────────
[ OK ]  Daily    H(TSA)                           1.7789  (expected: 1.7789)
[ OK ]  Daily    H(PSI)                           1.3091  (expected: 1.3091)
[ OK ]  Daily    PE(TSA)                          0.9045  (expected: 0.9045)
[ OK ]  Daily    PE(PSI)                          0.8231  (expected: 0.8231)
[ OK ]  Daily    LZC(TSA)                         0.1254  (expected: 0.1254)
[ OK ]  Daily    LZC(PSI)                         0.0987  (expected: 0.0987)
[ OK ]  Daily    I(TSA;PSI)                       0.7557  (expected: 0.7557)
[ OK ]  Monthly  H(TSA)                           2.7615  (expected: 2.7615)
[ OK ]  Monthly  H(PSI)                           2.6063  (expected: 2.6063)
[ OK ]  Monthly  PE(TSA)                          0.9973  (expected: 0.9973)
[ OK ]  Monthly  PE(PSI)                          0.9838  (expected: 0.9838)
[ OK ]  Monthly  LZC(TSA)                         0.3893  (expected: 0.3893)
[ OK ]  Monthly  LZC(PSI)                         0.3664  (expected: 0.3664)
[ OK ]  Monthly  I(TSA;PSI)                       2.0433  (expected: 2.0433)
[ OK ]  Annual   H(TSA)                           2.6258  (expected: 2.6258)
[ OK ]  Annual   H(PSI)                           2.5850  (expected: 2.585)
[ OK ]  Annual   PE(TSA)                          0.6520  (expected: 0.652)
[ OK ]  Annual   PE(PSI)                          0.6520  (expected: 0.652)
[ OK ]  Annual   LZC(TSA)                         0.7500  (expected: 0.75)
[ OK ]  Annual   LZC(PSI)                         0.7500  (expected: 0.75)
[ OK ]  Annual   I(TSA;PSI)                       2.3554  (expected: 2.3554)
[ OK ]  Guard qcut  H(TSA) daily ≠ log2(10)       1.778875  (expected: ≠ 3.3219)

────────────────────────────────────────────────────────────
BLOCK 2 — Bin stability (Cell 7)
────────────────────────────────────────────────────────────
[ OK ]  N_BINS                                    10  (expected: 10)
[ OK ]  MI(n=10) monthly                          2.0433

────────────────────────────────────────────────────────────
BLOCK 3 — Optimal window (Cell 9)
────────────────────────────────────────────────────────────
[ OK ]  WINDOW (months)                           26  (expected: 26)
[ OK ]  KneeLocator elbow                         6
[ OK ]  Note: no classic elbow after qcut; 26m via QBO

────────────────────────────────────────────────────────────
BLOCK 4 — df_dynamic columns (Cell 11)
────────────────────────────────────────────────────────────
[ OK ]  N 26-month windows                        106  (expected: 106)
[ OK ]  Column MI_lo                              
[ OK ]  Column MI_hi                              
[ OK ]  Column H_TSA_lo                           
[ OK ]  Column H_TSA_hi                           
[ OK ]  Column H_PSI_lo                           
[ OK ]  Column H_PSI_hi                           
[ OK ]  Column LZC_TSA_lo                         
[ OK ]  Column LZC_TSA_hi                         
[ OK ]  Column PE_TSA                             
[ OK ]  Column PE_PSI                             

────────────────────────────────────────────────────────────
BLOCK 5 — Mann-Whitney U (Cell 13)
────────────────────────────────────────────────────────────
[ OK ]  H_TSA        min=1.2302  max=2.6722       p=1.79e-10  (expected: p < 2e-10)
[ OK ]  H_PSI        min=1.0488  max=2.6637       p=1.71e-10  (expected: p < 2e-10)
[ OK ]  LZC_TSA      min=0.4322  max=0.6043       p=3.06e-11  (expected: p < 2e-10)
[ OK ]  LZC_PSI      min=0.4121  max=0.6179       p=6.04e-11  (expected: p < 2e-10)
[ OK ]  MI           min=0.9003  max=1.9925       p=1.37e-10  (expected: p < 2e-10)
[ OK ]  PE_TSA       min=0.9702  max=0.9752       p=8.08e-01  (expected: PE: no phase sep. (expected))
[ OK ]  PE_PSI       min=0.9268  max=0.9704       p=2.23e-07  (expected: PE: no phase sep. (expected))

────────────────────────────────────────────────────────────
BLOCK 6 — KS test phases (CELL KS)
────────────────────────────────────────────────────────────
[ OK ]  KS(MI)  D                                 0.3962  (expected: 0.3962 ±0.005)
[ OK ]  KS(MI)  p                                 0.0004  (expected: 0.0004 ±0.001)
[ OK ]  KS(LZC) D                                 0.3585  (expected: 0.3585 ±0.005)
[ OK ]  KS(LZC) p                                 0.0020  (expected: 0.0020 ±0.002)
[ OK ]  SC24_MAX (split)                          2014-06-01  (expected: 53/53 symmetric)
[ OK ]  Loop direction                            CW  (expected: CW)
[ OK ]  Closure gap                               10.2%  (expected: ~10%)

────────────────────────────────────────────────────────────
BLOCK 7 — Pearson r (Cell 17)
────────────────────────────────────────────────────────────
[ OK ]  r(H_TSA, LZC_TSA)                         0.965623  (expected: 0.9656 ±0.002)
[ OK ]  p-value                                   1.1357e-62  (expected: ~1.14e-62)

────────────────────────────────────────────────────────────
BLOCK 8 — summary_statistics.csv (Cell 18)
────────────────────────────────────────────────────────────
[ OK ]  N entries in reference table              48  (expected: 48)

────────────────────────────────────────────────────────────
BLOCK 9 — Output files
────────────────────────────────────────────────────────────
[ OK ]  1.png                                     
[ OK ]  2.png                                     
[ OK ]  3.png                                     
[ OK ]  4.png                                     
[ OK ]  5.png                                     
[ OK ]  6.png                                     
[ OK ]  7.png                                     
[ OK ]  summary_statistics.csv                    
[ OK ]  sliding_window_metrics.csv                

────────────────────────────────────────────────────────────
BLOCK F9 — Generated figures (F9-final)
────────────────────────────────────────────────────────────
[ OK ]  3.png  Fig. 3  window stability (QBO + sigma)EXISTS  (expected: EXISTS)
[ OK ]  4.png  Fig. 4  dynamic metrics + phase shadingEXISTS  (expected: EXISTS)
[ OK ]  6.png  Fig. 6  D_JS(t) + I(t) temporal panelsEXISTS  (expected: EXISTS)
[ OK ]  8.png  Fig. 8  C-H plane (→ 8.png via F11_RENAME)EXISTS  (expected: EXISTS)
[ OK ]  9.png  Fig. 9  I(t) + C_LMC(t) temporal hysteresisEXISTS  (expected: EXISTS)
[ OK ]  C_LMC_TSA maximum (Fig. 9 lower panel)    0.2371  (2016-09-30)  (expected: computed)
[ OK ]  Loop I×C_LMC direction                    CW  (expected: CW (expected))

────────────────────────────────────────────────────────────
BLOCK 10 — Extremes of the 26-month window
────────────────────────────────────────────────────────────
[ OK ]  H_TSA max                                 2.9210  (expected: 2.921)
[ OK ]  H_TSA min                                 0.6219  (expected: 0.6219)
[ OK ]  H_PSI max                                 2.9801  (expected: 2.9801)
[ OK ]  H_PSI min                                 0.6219  (expected: 0.6219)
[ OK ]  LZC_TSA max                               0.6538  (expected: 0.6538)
[ OK ]  LZC_TSA min                               0.3462  (expected: 0.3462)
[ OK ]  LZC_PSI max                               0.6923  (expected: 0.6923)
[ OK ]  LZC_PSI min                               0.3462  (expected: 0.3462)
[ OK ]  MI max                                    2.3357  (expected: 2.3357)
[ OK ]  MI min                                    0.4410  (expected: 0.441)
[ OK ]  PE_TSA max                                0.9941  (expected: 0.9941)
[ OK ]  PE_TSA min                                0.8794  (expected: 0.8794)
[ OK ]  PE_PSI max                                0.9941  (expected: 0.9941)
[ OK ]  PE_PSI min                                0.8659  (expected: 0.8659)

────────────────────────────────────────────────────────────
BLOCK 11 — C_LMC (F8b)
────────────────────────────────────────────────────────────
[ OK ]  Column C_LMC_TSA                          present  (expected: present)
[ OK ]  Column C_LMC_PSI                          present  (expected: present)
[ OK ]  Column H_norm_TSA                         present  (expected: present)
[ OK ]  Column H_norm_PSI                         present  (expected: present)
[ OK ]  Column D_JS_TSA                           present  (expected: present)
[ OK ]  Column D_JS_PSI                           present  (expected: present)
[ OK ]  df_dynamic total columns                  23  (expected: 23)
[ OK ]  summary_statistics.csv rows               48  (expected: 48)
[ OK ]  C_LMC_TSA maximum                         0.2371  (2016-09-30)  (expected: computed)
[ OK ]  C_LMC_TSA minimum                         0.1000  (2014-10-31)  (expected: computed)
[ OK ]  C_LMC_PSI maximum                         0.2316  (expected: computed)
[ OK ]  Theoretical C_max(H_norm) curves          1000 pts  (expected: >0 pts)
[ OK ]  H_TSA mean ≠ log2(10)                     2.2047  (expected: ≠ 3.3219)

────────────────────────────────────────────────────────────
FINAL SUMMARY
────────────────────────────────────────────────────────────
[ OK ]  All checks passed — zero failures         

Gate F9-final: PASSED
============================================================
```
