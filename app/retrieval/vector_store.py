import json
import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "data/faiss_index.bin"
)

with open(
    "data/shl_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)


def semantic_search(query, top_k=15):

    embedding = model.encode([query])

    embedding = np.array(
        embedding
    ).astype("float32")

    distances, indices = index.search(
        embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(catalog):
            results.append(catalog[idx])

    return results