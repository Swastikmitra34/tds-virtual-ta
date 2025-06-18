from bs4 import BeautifulSoup
from markdownify import markdownify as md

def html_to_markdown(html):
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", class_="post")
    if not content_div:
        return ""
    return md(str(content_div))
