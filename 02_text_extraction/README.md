# 02 — Text Extraction

## Overview

This stage converts the raw bill PDFs to plain-text files suitable for TF-IDF vectorization. Extraction was performed using `pdfplumber` (v0.10.2), which handles multi-column layouts and embedded fonts better than PyPDF2 for legislative documents. Each PDF is parsed page-by-page; extracted text is lowercased, stripped of page headers/footers using regex patterns specific to LegiScan-formatted statehouse PDFs, and written to a corresponding `.txt` file.

Three bills yielded zero usable characters and were excluded from all downstream analysis: Iowa SB 514, Iowa SB 561 (both 0-character extractions), and TN SB 600 (no PDF available). All other 188 bills produced clean text extractions confirmed by manual spot-check of a 10% random sample.

## Inputs

- Bill PDFs from `01_data_collection/` (one file per bill, naming convention: `State - BillID.pdf`)

## Outputs

- `extracted_texts/` — one `.txt` file per successfully extracted bill (188 files); naming convention mirrors PDF names
- Extraction log with per-bill character counts (available from author upon request)

## Scripts

The extraction script and post-processing cleaning functions are documented in **Appendix B of the thesis**. The script is available from the author upon request.

> **Note:** The `extracted_texts/` directory is excluded from version control (see `.gitignore`) to avoid storing indirectly copyrighted content. Contact the author for access to the extracted text corpus.
