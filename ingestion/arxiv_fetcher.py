import feedparser
import requests
from config import ARXIV_API, MAX_RESULTS

class ArxivFetcher:

    def fetch(self, query):

        url = f"{ARXIV_API}?search_query=all:{query}&start=0&max_results={MAX_RESULTS}"

        response = requests.get(url)

        feed = feedparser.parse(response.text)

        papers = []

        for entry in feed.entries:

            papers.append({
                "title": entry.title,
                "abstract": entry.summary,
                "link": entry.link,
                "source": "arxiv"
            })

        return papers