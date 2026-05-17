import json
import pickle

from rank_bm25 import BM25Okapi

with open(
    "data/shl_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)

documents = []

for item in catalog:

    text = (
        item["name"] + " " +
        item["description"] + " " +
        " ".join(item["skills"])
    )

    documents.append(text)

tokenized = [
    doc.lower().split()
    for doc in documents
]

bm25 = BM25Okapi(tokenized)

with open(
    "data/bm25.pkl",
    "wb"
) as f:

    pickle.dump(bm25, f)

print("BM25 saved")