import pickle
import json

with open(
    "data/bm25.pkl",
    "rb"
) as f:

    bm25 = pickle.load(f)

with open(
    "data/shl_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)


def keyword_search(query, top_k=15):

    tokenized = query.lower().split()

    scores = bm25.get_scores(tokenized)

    scored = list(
        enumerate(scores)
    )

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for idx, score in scored[:top_k]:
        results.append(catalog[idx])

    return results