# data/ — Analysis-Ready CSV Files

This directory contains all datasets used directly by the regression scripts and figures. Raw bill PDFs and intermediate extraction outputs are not versioned here; see the numbered pipeline directories for those.

---

## File Codebook

### `NoveltyScores_DEFINITIVE.csv` — 188 rows

Primary output of the TF-IDF pipeline. One row per successfully extracted bill.

| Column | Description |
|--------|-------------|
| `bill_id` | Unique bill identifier (format: `StateAbbrev_Chamber_Number`, e.g., `VT_S_37`) |
| `state` | Two-letter state abbreviation |
| `novelty_score_B` | **Option B cross-state novelty** — `1 − max(sim to any different-state bill)`. Primary DV. |
| `novelty_score_A` | Option A corpus novelty — `1 − max(sim to any other bill)`. Included for reference only. |
| `most_similar_crossstate_bill` | `bill_id` of the most-similar bill from a different state |
| `max_crossstate_similarity` | Raw cosine similarity to `most_similar_crossstate_bill` |

---

### `CrossState_Pairs_FINAL.csv` — 48 rows

All cross-state bill pairs with cosine similarity ≥ 0.30 (threshold selected to capture meaningful textual overlap while excluding noise).

| Column | Description |
|--------|-------------|
| `bill_id_A` | `bill_id` of the first bill in the pair |
| `state_A` | State of bill A |
| `bill_id_B` | `bill_id` of the second bill in the pair |
| `state_B` | State of bill B |
| `cosine_similarity` | Pairwise TF-IDF cosine similarity (0–1) |

Notable pairs: Vermont SB 37 appears in 10 pairs (protective hub); Nevada SB 370 / Washington HB 1155 = most similar cross-state pair (sim = 0.807).

---

### `SimilarityMatrix_FINAL.csv` — 188 rows × 189 columns

Full 188×188 pairwise cosine similarity matrix. The first column is `bill_id` (row labels); remaining 188 columns are `bill_id` values (column labels). Cell `[i, j]` = cosine similarity between bill *i* and bill *j*. Diagonal = 1.0 (self-similarity).

---

### `regression_data_R.csv` — 188 rows

Bill-level dataset used by `05_regression/regression_analysis.R`.

| Column | Description |
|--------|-------------|
| `bill_id` | Unique bill identifier |
| `state` | Two-letter state abbreviation |
| `novelty_score_B` | Option B cross-state novelty (DV) |
| `professionalism` | Squire Index score (continuous, 2021/2024 interpolated) |
| `government_control` | Partisan chamber alignment: `unified_dem`, `unified_rep`, `divided` |
| `direction` | Bill direction: `protective`, `restrictive`, `neutral` |
| `mechanism` | Primary policy mechanism: `proc_expansion`, `funding`, `provider_reg`, `gest_limit`, `other` |
| `log_advocacy` | Natural log of `state_advocacy_amount_total` (Stanford DIME 4.0; NA for 13 states) |
| `state_advocacy_amount_total` | Raw total state-level advocacy spending in dollars |

---

### `dyadic_dataset.csv` — 1,035 rows

State-pair dyadic dataset used by `05_regression/dyadic_regression.R`. One row per ordered state dyad.

| Column | Description |
|--------|-------------|
| `state_A` | Two-letter abbreviation for state A |
| `state_B` | Two-letter abbreviation for state B |
| `mean_crossstate_similarity` | Mean cosine similarity across all bill pairs between states A and B |
| `pac_jaccard` | Jaccard index of shared advocacy organization presence between states A and B (Stanford DIME 4.0) |
| `contiguous` | Binary: 1 if states A and B share a land border, 0 otherwise |
| `same_direction` | Binary: 1 if both states' modal bill direction is the same |
| `professionalism_diff` | Absolute difference in Squire Index scores |

---

### `VIF_Model3.csv` — 7 rows

Variance inflation factors for all predictors in Model 3 (M3), used to assess multicollinearity.

| Column | Description |
|--------|-------------|
| `predictor` | Predictor name as specified in M3 |
| `vif` | Variance inflation factor |

All VIF values < 5 (max = 4.64); no multicollinearity concern.

---

### `InfluentialObservations_Model3.csv` — 5 rows

Bills flagged as potentially influential by Cook's Distance in Model 3.

| Column | Description |
|--------|-------------|
| `bill_id` | Bill identifier |
| `state` | State abbreviation |
| `cooks_d` | Cook's Distance value |
| `novelty_score_B` | Option B novelty score for context |

Maximum Cook's D = 0.007; no observation is practically influential.
