import openai
import pickle
import faiss
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/embeddings.pkl", "rb") as f:
    index, metadata = pickle.load(f)

def query(question: str, top_k=5):
    question_embedding = embedder.encode([question])
    D, I = index.search(question_embedding, top_k)

    context_chunks = [metadata[i]["text"] for i in I[0]]
    urls = [
        {"url": metadata[i].get("url", ""), "text": metadata[i].get("title", "Reference")}
        for i in I[0]
    ]

    context = "\n\n".join(context_chunks)

    prompt = f"""You are a helpful virtual TA for the TDS course.
Use the context below to answer the question:

Context:
{context}

Question:
{question}

Answer:"""
