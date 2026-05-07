# 04 — Novelty Calculations

## Overview

This stage derives bill-level novelty scores from the 188×188 cosine similarity matrix. The thesis uses **Option B (cross-state novelty)** as the primary measure throughout all regression models. Option B captures how textually distinctive each bill is relative to bills from *other* states, which is the quantity of interest for studying interstate policy diffusion.

**Option B (cross-state novelty):**

```
novelty_B(i) = 1 − max{ sim(i, j) : j ≠ i AND state(j) ≠ state(i) }
```

Each bill's novelty score is one minus the maximum cosine similarity it shares with any bill from a *different* state. Higher values indicate greater textual distinctiveness (less cross-state borrowing). Lower values indicate closer alignment with legislation in another state.

For reference, the corpus-level (Option A) novelty — `1 − max{ sim(i,j) : j ≠ i }` — is also included in `NoveltyScores_DEFINITIVE.csv` but is not used as the primary DV.

## Corpus Summary (Option B)

- N = 188 bills, 46 states
- Mean = 0.769, SD = 0.122
- Distribution: <0.50: 2 (1.1%) | 0.50–0.69: 43 (22.9%) | 0.70–0.89: 125 (66.5%) | ≥0.90: 18 (9.6%)

## Inputs

- `data/SimilarityMatrix_FINAL.csv` — 188×188 cosine similarity matrix from Stage 03
- `data/Bills_2023_Master_Coded.csv` — state identifiers for each bill

## Outputs

- `data/NoveltyScores_DEFINITIVE.csv` — one row per bill with Option A and Option B novelty scores, plus the identity of the most-similar cross-state bill

## Scripts

The novelty scoring procedure is documented in **Appendix B of the thesis** and is also embedded in `03_tfidf_analysis/rerun_tfidf_quick.py` (which writes `NoveltyScores_DEFINITIVE.csv` as a secondary output). The standalone scoring script is available from the author upon request.
