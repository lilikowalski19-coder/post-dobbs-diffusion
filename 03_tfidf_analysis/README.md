# 03 — TF-IDF Analysis

## Overview

This stage fits a TF-IDF (term frequency–inverse document frequency) model on the 188-bill corpus and computes pairwise cosine similarity to produce the 188×188 similarity matrix. The vectorizer uses unigrams, bigrams, and trigrams (`ngram_range=(1,3)`) with English stopword removal, document-frequency filtering (`min_df=2`, `max_df=0.8`), and no maximum-features cap — yielding 104,445 unique n-gram features. Cosine similarity is then computed across all bill pairs, and the resulting dense matrix is saved to `data/SimilarityMatrix_FINAL.csv`.

## TF-IDF Parameters (Definitive)

```python
TfidfVectorizer(
    min_df=2,
    max_df=0.8,
    ngram_range=(1, 3),
    stop_words='english'
)
# No max_features cap → 104,445 features
```

These parameters are the definitive settings used throughout the thesis. Do not alter them without updating all downstream novelty scores.

## Inputs

- `02_text_extraction/extracted_texts/` — 188 `.txt` files (one per bill)
- Bill metadata (state identifiers) from `data/Bills_2023_Master_Coded.csv`

## Outputs

- `data/SimilarityMatrix_FINAL.csv` — 188×188 pairwise cosine similarity matrix (bill IDs as row/column headers)

## Script

`rerun_tfidf_quick.py` — Self-contained Python script that reads extracted texts, fits the TF-IDF model with the definitive parameters, computes the cosine similarity matrix, and writes it to `data/`.

```bash
python 03_tfidf_analysis/rerun_tfidf_quick.py \
    --texts_dir 02_text_extraction/extracted_texts/ \
    --metadata  data/Bills_2023_Master_Coded.csv \
    --output_dir data/
```

Expected runtime: ~2 minutes on a modern laptop for 188 bills.
