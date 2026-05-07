"""
Replication script: TF-IDF similarity matrix and Option B novelty scores.

Reads per-bill .txt files from an extracted-texts directory and bill metadata
(for state identifiers), fits the definitive TF-IDF vectorizer, computes the
188x188 cosine similarity matrix, derives Option B cross-state novelty scores,
and writes both outputs to the data/ directory.

Usage:
    python 03_tfidf_analysis/rerun_tfidf_quick.py \
        --texts_dir 02_text_extraction/extracted_texts/ \
        --metadata  data/Bills_2023_Master_Coded.csv \
        --output_dir data/

Expected runtime: ~2 minutes on a modern laptop for 188 bills.
"""

import argparse
import os
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------------------------
# Definitive TF-IDF parameters — do not change without updating all outputs
# ---------------------------------------------------------------------------
TFIDF_PARAMS = dict(
    min_df=2,
    max_df=0.8,
    ngram_range=(1, 3),
    stop_words="english",
    # No max_features cap → 104,445 features on the thesis corpus
)

SIMILARITY_THRESHOLD = 0.30  # for CrossState_Pairs output


def load_texts(texts_dir: str, bill_ids: list[str]) -> tuple[list[str], list[str]]:
    """Load .txt files matching bill_ids; return (texts, valid_bill_ids)."""
    texts, valid_ids = [], []
    missing = []
    for bid in bill_ids:
        # Try exact match first, then with common naming variants
        candidates = [
            os.path.join(texts_dir, f"{bid}.txt"),
        ]
        # Also try replacing underscores with " - " (LegiScan PDF naming)
        candidates.append(os.path.join(texts_dir, bid.replace("_", " - ") + ".txt"))

        found = None
        for c in candidates:
            if os.path.isfile(c):
                found = c
                break

        if found is None:
            missing.append(bid)
            continue

        with open(found, encoding="utf-8", errors="replace") as f:
            text = f.read().strip()

        if len(text) < 50:
            print(f"  WARN: {bid} has only {len(text)} chars — skipping")
            missing.append(bid)
            continue

        texts.append(text)
        valid_ids.append(bid)

    if missing:
        print(f"  Skipped {len(missing)} bills (missing or near-empty): {missing[:5]}{'...' if len(missing) > 5 else ''}")

    return texts, valid_ids


def compute_similarity_matrix(texts: list[str]) -> tuple[np.ndarray, TfidfVectorizer]:
    print("  Fitting TF-IDF vectorizer...")
    t0 = time.time()
    vectorizer = TfidfVectorizer(**TFIDF_PARAMS)
    tfidf_matrix = vectorizer.fit_transform(texts)
    n_features = tfidf_matrix.shape[1]
    print(f"  Vectorizer fitted: {n_features:,} features, {tfidf_matrix.shape[0]} documents ({time.time()-t0:.1f}s)")

    print("  Computing pairwise cosine similarity...")
    t0 = time.time()
    sim_matrix = cosine_similarity(tfidf_matrix, dense_output=True)
    print(f"  Similarity matrix computed ({time.time()-t0:.1f}s)")

    return sim_matrix, vectorizer


def compute_novelty_b(sim_matrix: np.ndarray, bill_ids: list[str], states: pd.Series) -> pd.DataFrame:
    """
    Option B (cross-state novelty): 1 - max(similarity to any different-state bill).
    Also records the identity and similarity of the most similar cross-state bill.
    """
    state_arr = np.array([states[bid] for bid in bill_ids])
    n = len(bill_ids)

    novelty_b = np.zeros(n)
    max_cross_sim = np.zeros(n)
    most_similar_bill = [""] * n

    for i in range(n):
        # Mask: same-state bills and self
        cross_state_mask = (state_arr != state_arr[i])
        cross_state_mask[i] = False

        if cross_state_mask.sum() == 0:
            novelty_b[i] = 1.0
            continue

        cross_sims = sim_matrix[i, cross_state_mask]
        max_sim = cross_sims.max()
        max_cross_sim[i] = max_sim
        novelty_b[i] = 1.0 - max_sim

        # Identify the most similar cross-state bill
        cross_indices = np.where(cross_state_mask)[0]
        best_j = cross_indices[cross_sims.argmax()]
        most_similar_bill[i] = bill_ids[best_j]

    return pd.DataFrame({
        "bill_id": bill_ids,
        "state": [state_arr[i] for i in range(n)],
        "novelty_score_B": novelty_b,
        "max_crossstate_similarity": max_cross_sim,
        "most_similar_crossstate_bill": most_similar_bill,
    })


def compute_novelty_a(sim_matrix: np.ndarray, bill_ids: list[str]) -> np.ndarray:
    """Option A (corpus novelty): 1 - max(similarity to any other bill)."""
    sim_copy = sim_matrix.copy()
    np.fill_diagonal(sim_copy, 0.0)
    return 1.0 - sim_copy.max(axis=1)


def extract_cross_state_pairs(
    sim_matrix: np.ndarray,
    bill_ids: list[str],
    states: pd.Series,
    threshold: float = SIMILARITY_THRESHOLD,
) -> pd.DataFrame:
    state_arr = np.array([states[bid] for bid in bill_ids])
    rows = []
    n = len(bill_ids)
    for i in range(n):
        for j in range(i + 1, n):
            if state_arr[i] == state_arr[j]:
                continue
            s = sim_matrix[i, j]
            if s >= threshold:
                rows.append({
                    "bill_id_A": bill_ids[i],
                    "state_A": state_arr[i],
                    "bill_id_B": bill_ids[j],
                    "state_B": state_arr[j],
                    "cosine_similarity": round(s, 6),
                })
    df = pd.DataFrame(rows).sort_values("cosine_similarity", ascending=False).reset_index(drop=True)
    return df


def main():
    parser = argparse.ArgumentParser(description="Rerun TF-IDF analysis for post-Dobbs diffusion thesis.")
    parser.add_argument("--texts_dir", default="02_text_extraction/extracted_texts/",
                        help="Directory containing per-bill .txt files")
    parser.add_argument("--metadata", default="data/Bills_2023_Master_Coded.csv",
                        help="Master CSV with bill_id and state columns")
    parser.add_argument("--output_dir", default="data/",
                        help="Directory where output CSVs will be written")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Load metadata
    print(f"Loading metadata from {args.metadata}...")
    meta = pd.read_csv(args.metadata)
    if "bill_id" not in meta.columns or "state" not in meta.columns:
        raise ValueError("Metadata CSV must have 'bill_id' and 'state' columns.")
    state_lookup = meta.set_index("bill_id")["state"].to_dict()
    bill_ids_all = meta["bill_id"].tolist()
    print(f"  {len(bill_ids_all)} bills in metadata")

    # Load texts
    print(f"\nLoading extracted texts from {args.texts_dir}...")
    texts, valid_ids = load_texts(args.texts_dir, bill_ids_all)
    print(f"  {len(valid_ids)} bills with usable text")

    states = pd.Series(state_lookup)

    # TF-IDF + similarity matrix
    print("\nRunning TF-IDF pipeline...")
    sim_matrix, _ = compute_similarity_matrix(texts)

    # Option B novelty
    print("\nComputing Option B (cross-state) novelty scores...")
    novelty_df = compute_novelty_b(sim_matrix, valid_ids, states)
    novelty_a = compute_novelty_a(sim_matrix, valid_ids)
    novelty_df.insert(3, "novelty_score_A", novelty_a)

    out_novelty = os.path.join(args.output_dir, "NoveltyScores_DEFINITIVE.csv")
    novelty_df.to_csv(out_novelty, index=False)
    print(f"  Saved: {out_novelty} ({len(novelty_df)} rows)")
    print(f"  Option B — mean: {novelty_df.novelty_score_B.mean():.3f}, SD: {novelty_df.novelty_score_B.std():.3f}")

    # Cross-state pairs
    print(f"\nExtracting cross-state pairs (threshold >= {SIMILARITY_THRESHOLD})...")
    pairs_df = extract_cross_state_pairs(sim_matrix, valid_ids, states)
    out_pairs = os.path.join(args.output_dir, "CrossState_Pairs_FINAL.csv")
    pairs_df.to_csv(out_pairs, index=False)
    print(f"  Saved: {out_pairs} ({len(pairs_df)} pairs)")

    # Full similarity matrix
    print("\nSaving similarity matrix...")
    sim_df = pd.DataFrame(sim_matrix, index=valid_ids, columns=valid_ids)
    sim_df.index.name = "bill_id"
    out_sim = os.path.join(args.output_dir, "SimilarityMatrix_FINAL.csv")
    sim_df.to_csv(out_sim)
    print(f"  Saved: {out_sim} ({len(valid_ids)}x{len(valid_ids)})")

    print("\nDone.")


if __name__ == "__main__":
    main()
