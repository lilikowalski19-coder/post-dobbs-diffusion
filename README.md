# Networks of Influence: Legislative Text Diffusion in State Reproductive Policy After *Dobbs*

**Liliana Kowalski**
B.A. Political Science, University of Wisconsin–Madison
Honors Thesis, May 2026
Advisor: Prof. Eleanor Neff Powell

---

## Abstract

This thesis examines how abortion-related legislation diffused across U.S. states in the first full legislative year after *Dobbs v. Jackson Women's Health Organization* (2022). Using a corpus of 188 enacted bills across 46 states, it employs TF-IDF cosine similarity (104,445 unique n-grams), bill-level OLS regression, and dyadic regression to identify structural predictors of textual convergence. The analysis finds that protective coalitions deployed standardized legislative templates more aggressively than restrictive ones, that shared advocacy organization co-presence is a significant predictor of cross-state similarity, and that geographic contiguity is null — suggesting that coordinating actors, not spatial proximity, drive post-*Dobbs* policy diffusion.

---

## Key Findings

- Protective coalitions deployed standardized templates more aggressively than restrictive ones (Protective β = −0.076, *p* = 0.022)
- Shared advocacy organization co-presence predicts cross-state similarity (PAC Jaccard β = +0.039, *p* < 0.001)
- Geographic contiguity is null (β = +0.003, *p* = 0.734)
- Highest textual coordination coexists with zero common PAC donors between coordinated legislators, pointing to organizational intermediaries rather than direct donor networks as the transmission mechanism

---

## Data Sources

| Source | Use |
|--------|-----|
| [LegiScan](https://legiscan.com/) | Bill texts (PDFs) for 2023 legislative sessions |
| [Stanford DIME 4.0](https://data.stanford.edu/dime) | Campaign finance / advocacy spending |
| Squire Index 2021/2024 | Legislative professionalism scores |
| [NCSL](https://www.ncsl.org/) | Partisan chamber alignment (unified/divided) |
| [Guttmacher Institute](https://www.guttmacher.org/) | Policy direction classification validation |

> **Note on bill texts:** Raw bill PDFs are not included in this repository due to copyright and file-size constraints. Bill texts are available directly from [LegiScan](https://legiscan.com/). See `01_data_collection/README.md` for the retrieval protocol.

---

## Software Environment

**Python 3.11.4**

| Package | Version | Use |
|---------|---------|-----|
| pdfplumber | 0.10.2 | PDF text extraction |
| scikit-learn | 1.3.0 | TF-IDF vectorization, cosine similarity |
| pandas | 2.0.3 | Data manipulation |
| numpy | 1.24.3 | Matrix operations |
| nltk | 3.8.1 | Stopword lists |

See `requirements.txt` for the full pinned environment. Install with:

```bash
pip install -r requirements.txt
```

**R 4.x**

| Package | Use |
|---------|-----|
| tidyverse | Data wrangling and visualization |
| ggplot2 | All thesis figures |
| estimatr | Bell-McCaffrey CR2 Satterthwaite standard errors |

---

## Repository Structure

```
post-dobbs-diffusion/
├── 01_data_collection/    Bill inventory and LegiScan retrieval protocol
├── 02_text_extraction/    PDF-to-text extraction pipeline (pdfplumber)
├── 03_tfidf_analysis/     TF-IDF vectorization and 188×188 cosine similarity matrix
├── 04_novelty_calculations/  Cross-state (Option B) novelty score derivation
├── 05_regression/         OLS bill-level models (M1–M3) and dyadic models (D1–D3)
├── 06_coding/             Manual coding protocol and intercoder reliability
├── data/                  All analysis-ready CSV files (see data/README.md for codebook)
├── figures/               Publication-quality PDF figures (Fig. 4.1–4.7)
└── thesis/                LaTeX source for full thesis manuscript
```

### Analytical pipeline

The six numbered directories document the pipeline in execution order:

1. **`01_data_collection/`** — Bill list construction and LegiScan retrieval
2. **`02_text_extraction/`** — PDF parsing with `pdfplumber`; outputs per-bill `.txt` files
3. **`03_tfidf_analysis/`** — TF-IDF fitting and pairwise cosine similarity computation
4. **`04_novelty_calculations/`** — Cross-state novelty scoring (Option B: `1 − max cross-state similarity`)
5. **`05_regression/`** — Statistical modeling; scripts run directly against `data/` CSVs
6. **`06_coding/`** — Manual coding of bill direction, mechanism, and advocacy linkages

### Reproducing regressions

The regression scripts in `05_regression/` are self-contained and run directly against the CSV files in `data/`:

```r
# From the repo root in R:
source("05_regression/regression_analysis.R")   # Models M1–M3
source("05_regression/dyadic_regression.R")      # Models D1–D3
```

### Regenerating the TF-IDF similarity matrix

With per-bill `.txt` files in place (see `02_text_extraction/`), the similarity matrix can be regenerated:

```bash
python 03_tfidf_analysis/rerun_tfidf_quick.py \
    --texts_dir 02_text_extraction/extracted_texts/ \
    --output_dir data/
```

This reproduces `SimilarityMatrix_FINAL.csv` and `NoveltyScores_DEFINITIVE.csv`.

---

## Citation

```bibtex
@thesis{kowalski2026networks,
  author    = {Kowalski, Liliana},
  title     = {Networks of Influence: Legislative Text Diffusion in State
               Reproductive Policy After {Dobbs}},
  school    = {University of Wisconsin--Madison},
  year      = {2026},
  month     = {may},
  type      = {Honors Thesis},
  note      = {Department of Political Science. Advisor: Prof. Eleanor Neff Powell}
}
```

---

## Contact

Liliana Kowalski
University of Wisconsin–Madison, Department of Political Science
[lilianakowalskipolicy@gmail.com](mailto:lilianakowalskipolicy@gmail.com)

