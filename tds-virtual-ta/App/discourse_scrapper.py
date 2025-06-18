import requests
from bs4 import BeautifulSoup
import json
import os

DISCOURSE_BASE = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORIES = ["tools-in-data-science", "assignments", "projects"]

headers = {
    "Cookie": os.getenv("DISCOURSE_COOKIE")
}

def scrape_posts():
    posts = []
    for category in CATEGORIES:
        url = f"{DISCOURSE_BASE}/c/{category}.json"
        r = requests.get(url, headers=headers)
        for topic in r.json().get("topic_list", {}).get("topics", []):
            topic_id = topic["id"]
            topic_url = f"{DISCOURSE_BASE}/t/{topic_id}.json"
            topic_res = requests.get(topic_url, headers=headers)
            posts.append(topic_res.json())

    with open("data/discourse_data.json", "w") as f:
        json.dump(posts, f)

### rag/embed.py
import json
import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = SentenceTransformer('all-MiniLM-L6-v2')

with open("data/discourse_data.json") as f:
    data = json.load(f)

texts = []
metadatas = []
for topic in data:
    for post in topic.get("post_stream", {}).get("posts", []):
        texts.append(post["cooked"])
        metadatas.append({"url": f"{DISCOURSE_BASE}/t/{topic['slug']}/{topic['id']}", "text": post["cooked"][:100]})

embeddings = model.encode(texts)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

faiss.write_index(index, "data/faiss_index/index.faiss")
with open("data/faiss_index/meta.json", "w") as f:
    json.dump(metadatas, f)
