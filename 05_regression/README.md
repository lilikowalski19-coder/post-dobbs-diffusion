# 05 — Regression Analysis

## Overview

This stage contains all statistical models reported in Chapter 4 of the thesis. Two separate R scripts implement the bill-level OLS models and the dyadic regression models, respectively. All models use Bell-McCaffrey CR2 Satterthwaite standard errors (via the `estimatr` package) clustered at the state level to account for within-state correlation across bills.

## Bill-Level Models (`regression_analysis.R`)

Three nested OLS models with DV = Option B cross-state novelty score (N=188 for M1–M2; N=175 for M3 due to missing advocacy spending data).

| Model | Covariates | N | R² |
|-------|-----------|---|-----|
| M1 | professionalism + government_control | 188 | 0.085 |
| M2 | + direction + mechanism | 188 | 0.156 |
| M3 | + log(state_advocacy_amount_total) | 175 | 0.150 |

**Key findings:**
- Professionalism: β = −0.155 (*p* = 0.006) — more professional legislatures produce less novel bills (policy learning)
- Unified Democratic vs. Divided: β = +0.145 (*p* = 0.009)
- Unified Republican vs. Divided: β = +0.071 (*p* = 0.032)
- Protective vs. Neutral: β = −0.076 (*p* = 0.008) — less novel (coordinated post-*Dobbs* response)
- Restrictive vs. Neutral: not significant (*p* = 0.46)
- Procedural Expansion mechanism: β = +0.125 (*p* = 0.0003) — most novel mechanism
- Advocacy spending: null (*p* = 0.270)
- All VIF < 5 (max = 4.64); 5 flagged Cook's D observations, max = 0.007 (not practically influential)

## Dyadic Models (`dyadic_regression.R`)

Three nested OLS models with DV = pairwise cosine similarity (N=1,035 state-pair dyads). All models cluster standard errors by state-pair.

## Running the Scripts

```r
# Install dependencies if needed:
install.packages(c("tidyverse", "ggplot2", "estimatr"))

# Run from repo root:
source("05_regression/regression_analysis.R")
source("05_regression/dyadic_regression.R")
```

Scripts read from `data/regression_data_R.csv` and `data/dyadic_dataset.csv` respectively.
