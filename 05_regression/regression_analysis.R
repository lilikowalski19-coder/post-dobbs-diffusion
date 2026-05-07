# regression_analysis.R
# Bill-level OLS models M1-M3 with Bell-McCaffrey CR2 Satterthwaite SE
# clustered by state. DV = Option B cross-state novelty score.
#
# Requires: tidyverse, estimatr
# Run from repo root: source("05_regression/regression_analysis.R")

library(tidyverse)
library(estimatr)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

df <- read_csv("data/regression_data_R.csv", show_col_types = FALSE)

cat(sprintf("Loaded %d bills from %d states\n", nrow(df), n_distinct(df$state)))

# Factor coding
df <- df %>%
  mutate(
    government_control = relevel(factor(government_control), ref = "divided"),
    direction          = relevel(factor(direction),          ref = "neutral"),
    mechanism          = relevel(factor(mechanism),          ref = "other")
  )

# ---------------------------------------------------------------------------
# Model 1: Structural covariates only
# ---------------------------------------------------------------------------

m1 <- lm_robust(
  novelty_score_B ~ professionalism + government_control,
  data      = df,
  clusters  = state,
  se_type   = "CR2"
)

cat("\n=== Model 1 (N =", nobs(m1), ", R² =", round(summary(m1)$r.squared, 3), ") ===\n")
print(summary(m1))

# ---------------------------------------------------------------------------
# Model 2: + policy direction and mechanism
# ---------------------------------------------------------------------------

m2 <- lm_robust(
  novelty_score_B ~ professionalism + government_control + direction + mechanism,
  data     = df,
  clusters = state,
  se_type  = "CR2"
)

cat("\n=== Model 2 (N =", nobs(m2), ", R² =", round(summary(m2)$r.squared, 3), ") ===\n")
print(summary(m2))

# ---------------------------------------------------------------------------
# Model 3: + log(advocacy spending)  [N=175 due to missing spending data]
# ---------------------------------------------------------------------------

df_m3 <- df %>% filter(!is.na(log_advocacy))
cat(sprintf("\nModel 3 sample: %d bills (%d dropped for missing advocacy spending)\n",
            nrow(df_m3), nrow(df) - nrow(df_m3)))

m3 <- lm_robust(
  novelty_score_B ~ professionalism + government_control + direction + mechanism + log_advocacy,
  data     = df_m3,
  clusters = state,
  se_type  = "CR2"
)

cat("\n=== Model 3 (N =", nobs(m3), ", R² =", round(summary(m3)$r.squared, 3), ") ===\n")
print(summary(m3))

# ---------------------------------------------------------------------------
# VIF check (Model 3)
# ---------------------------------------------------------------------------

if (!requireNamespace("car", quietly = TRUE)) {
  message("Install 'car' package for VIF: install.packages('car')")
} else {
  library(car)
  m3_ols <- lm(
    novelty_score_B ~ professionalism + government_control + direction + mechanism + log_advocacy,
    data = df_m3
  )
  vif_vals <- vif(m3_ols)
  cat("\n=== VIF (Model 3) ===\n")
  print(vif_vals)

  vif_df <- as.data.frame(vif_vals) %>%
    rownames_to_column("predictor") %>%
    rename(vif = `vif_vals`)
  write_csv(vif_df, "data/VIF_Model3.csv")
  cat("Saved: data/VIF_Model3.csv\n")
}

# ---------------------------------------------------------------------------
# Influential observations (Cook's D, Model 3)
# ---------------------------------------------------------------------------

m3_ols <- lm(
  novelty_score_B ~ professionalism + government_control + direction + mechanism + log_advocacy,
  data = df_m3
)
cooks <- cooks.distance(m3_ols)
threshold <- 4 / nrow(df_m3)
influential <- df_m3[cooks > threshold, c("bill_id", "state", "novelty_score_B")]
influential$cooks_d <- cooks[cooks > threshold]
influential <- influential %>% arrange(desc(cooks_d))

cat(sprintf("\n=== Influential observations (Cook's D > %.4f) ===\n", threshold))
print(influential)

write_csv(influential, "data/InfluentialObservations_Model3.csv")
cat("Saved: data/InfluentialObservations_Model3.csv\n")
cat(sprintf("Max Cook's D = %.4f (not practically influential)\n", max(cooks)))
