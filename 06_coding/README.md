# 06 — Manual Coding

## Overview

This stage documents the manual coding of bill-level covariates that cannot be derived computationally from bill text alone. Three variables were coded by hand: (1) **direction** — whether each bill is protective (expands abortion access), restrictive (limits access), or neutral/administrative; (2) **mechanism** — the primary policy mechanism invoked (e.g., procedural expansion, funding, provider regulation, gestational limit); and (3) **advocacy linkages** — whether each bill can be connected to known model legislation or advocacy organization templates (ALEC, NARAL/PPFA affiliate networks, etc.).

A 10% random subsample (N=19 bills) was double-coded by a second coder to assess intercoder reliability. Cohen's κ ≥ 0.82 for all three variables, meeting the threshold for substantial agreement.

Finalized codes are stored as columns in `data/Bills_2023_Master_Coded.csv` and are carried through to `data/regression_data_R.csv`.

## Inputs

- Bill texts from `02_text_extraction/extracted_texts/`
- Guttmacher Institute 2023 policy tracker (used as anchor for direction coding)
- ALEC model legislation archive (for advocacy linkage coding)

## Outputs

- Coded columns (`direction`, `mechanism`, `advocacy_link`) in `data/Bills_2023_Master_Coded.csv`

## Codebook and Protocol

The full coding protocol, decision rules, and edge cases are documented in **Appendix B of the thesis**. The codebook and double-coding data are available from the author upon request.
