# dyadic_regression.R
# Dyadic OLS models D1-D3: DV = mean cross-state cosine similarity between
# state-pair dyads (N=1,035). Standard errors clustered by state pair using
# Bell-McCaffrey CR2 Satterthwaite degrees of freedom (estimatr).
#
# Requires: tidyverse, estimatr
# Run from repo root: source("05_regression/dyadic_regression.R")

library(tidyverse)
library(estimatr)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

dyad <- read_csv("data/dyadic_dataset.csv", show_col_types = FALSE)

cat(sprintf("Loaded %d state-pair dyads\n", nrow(dyad)))

# Cluster ID: unordered state pair (A-B == B-A for two-way clustering)
dyad <- dyad %>%
  mutate(pair_id = paste(pmin(state_A, state_B), pmax(state_A, state_B), sep = "-"))

# ---------------------------------------------------------------------------
# Model D1: Geographic and alignment predictors only
# ---------------------------------------------------------------------------

d1 <- lm_robust(
  mean_crossstate_similarity ~ contiguous + same_direction + professionalism_diff,
  data     = dyad,
  clusters = pair_id,
  se_type  = "CR2"
)

cat("\n=== Model D1 (N =", nobs(d1), ", R² =", round(summary(d1)$r.squared, 3), ") ===\n")
print(summary(d1))

# ---------------------------------------------------------------------------
# Model D2: + PAC Jaccard (shared advocacy organization presence)
# ---------------------------------------------------------------------------

d2 <- lm_robust(
  mean_crossstate_similarity ~ contiguous + same_direction + professionalism_diff + pac_jaccard,
  data     = dyad,
  clusters = pair_id,
  se_type  = "CR2"
)

cat("\n=== Model D2 (N =", nobs(d2), ", R² =", round(summary(d2)$r.squared, 3), ") ===\n")
print(summary(d2))

# ---------------------------------------------------------------------------
# Model D3: Full specification
# ---------------------------------------------------------------------------

d3 <- lm_robust(
  mean_crossstate_similarity ~ contiguous + same_direction + professionalism_diff + pac_jaccard,
  data     = dyad %>% filter(!is.na(pac_jaccard)),
  clusters = pair_id,
  se_type  = "CR2"
)

cat("\n=== Model D3 (N =", nobs(d3), ", R² =", round(summary(d3)$r.squared, 3), ") ===\n")
print(summary(d3))

# ---------------------------------------------------------------------------
# Summary table: key coefficients
# ---------------------------------------------------------------------------

cat("\n=== Key coefficients summary ===\n")
cat("Contiguous (D1):      beta =", round(coef(d1)["contiguous"], 4),
    " p =", round(tidy(d1) %>% filter(term == "contiguous") %>% pull(p.value), 3), "\n")
cat("PAC Jaccard (D2):     beta =", round(coef(d2)["pac_jaccard"], 4),
    " p =", round(tidy(d2) %>% filter(term == "pac_jaccard") %>% pull(p.value), 4), "\n")
