import httpx
from bs4 import BeautifulSoup
import os
from App.utils import html_to_markdown
from dotenv import load_dotenv
load_dotenv()


LOGIN_URL = "https://discourse.onlinedegree.iitm.ac.in/session"
BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
USERNAME = os.getenv("DISCOURSE_USER")
PASSWORD = os.getenv("DISCOURSE_PASS")

client = httpx.Client(follow_redirects=True)

def login():
    resp = client.get(LOGIN_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.find("input", {"name": "authenticity_token"})["value"]

    login_data = {
        "login": USERNAME,
        "password": PASSWORD,
        "authenticity_token": csrf
    }

    client.post(LOGIN_URL, data=login_data)

def scrape_topics(category_slug, limit=50):
    login()
    topic_urls = []
    r = client.get(f"{BASE_URL}/c/{category_slug}.json")
    topics = r.json()["topic_list"]["topics"][:limit]

    for topic in topics:
        topic_id = topic["id"]
        slug = topic["slug"]
        url = f"{BASE_URL}/t/{slug}/{topic_id}"
        html = client.get(url).text
        markdown = html_to_markdown(html)

        with open(f"data/markdown/{slug}.md", "w", encoding="utf-8") as f:
            f.write(markdown)
