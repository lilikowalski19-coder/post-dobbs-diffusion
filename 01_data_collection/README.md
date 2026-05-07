# 01 — Data Collection

## Overview

This stage constructs the bill corpus: identifying in-scope legislation, assembling a bill inventory, and retrieving bill text PDFs. The population is all abortion-related legislation enacted in U.S. state legislatures during the 2023 regular legislative session (January–December 2023), across all 50 states. Bills were identified through LegiScan's full-text search and keyword filtering, then cross-validated against Guttmacher Institute tracking data to reduce false negatives.

Starting from 209 candidate bills, three extraction failures reduced the analyzable corpus to **188 bills across 46 states**. Failures: Iowa SB 514 (0 extracted characters), Iowa SB 561 (0 extracted characters), TN SB 600 (no PDF available on LegiScan).

## Inputs

- LegiScan session search results (keyword: "abortion", 2023 sessions)
- Guttmacher Institute 2023 state policy tracking spreadsheet (used for cross-validation only)

## Outputs

- `Bills_2023_Master_Coded.csv` (in `data/`) — 190-row master bill inventory with all covariates
- PDF files for 188 bills, stored locally (not versioned; see note below)

## Scripts

The retrieval protocol is documented in **Appendix B of the thesis**. The LegiScan API key and session query parameters are required to reproduce retrieval from scratch. Scripts are available from the author upon request.

> **Note:** Raw bill PDFs are not included in this repository due to copyright restrictions and file size. Bill texts can be retrieved directly from [LegiScan](https://legiscan.com/) using the bill IDs in `data/Bills_2023_Master_Coded.csv`.
