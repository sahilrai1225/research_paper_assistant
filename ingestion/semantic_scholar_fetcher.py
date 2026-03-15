import requests
from config import SEMANTIC_API

class SemanticScholarFetcher:

    def search(self, query):

        url = f"{SEMANTIC_API}/paper/search"

        params = {
            "query": query,
            "limit": 20,
            "fields": "title,abstract,year,citationCount"
        }

        response = requests.get(url, params=params)

        data = response.json()

        papers = []

        for p in data.get("data", []):

            papers.append({
                "title": p.get("title"),
                "abstract": p.get("abstract"),
                "year": p.get("year"),
                "citations": p.get("citationCount"),
                "source": "semantic"
            })

        return papers