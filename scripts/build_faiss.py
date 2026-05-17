import json
import pickle

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

with open(
    "data/shl_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)

documents = []

metadata = []

for item in catalog:

    text = f"""
    Name: {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Test Type:
    {item.get('test_type', '')}

    Job Levels:
    {item.get('job_levels', '')}

    Languages:
    {item.get('languages', '')}
    """

    documents.append(text)

    metadata.append(item)

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

embeddings = np.array(
    embeddings,
    dtype="float32"
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    "data/faiss.index"
)

with open(
    "data/metadata.pkl",
    "wb"
) as f:

    pickle.dump(metadata, f)

print("Embeddings built successfully")