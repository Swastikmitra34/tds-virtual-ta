import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
markdown_dir = "data/markdown"
texts, metadata = [], []

for fname in os.listdir(markdown_dir):
    path = os.path.join(markdown_dir, fname)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    texts.append(text)
    metadata.append({"filename": fname, "text": text})

embeddings = model.encode(texts)
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(embeddings)

with open("data/embeddings.pkl", "wb") as f:
    pickle.dump((index, metadata), f)

