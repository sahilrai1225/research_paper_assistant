from ingestion.arxiv_fetcher import ArxivFetcher
from ingestion.semantic_scholar_fetcher import SemanticScholarFetcher

class PaperPipeline:

    def __init__(self):

        self.arxiv = ArxivFetcher()

        self.semantic = SemanticScholarFetcher()

    def run(self, query):

        papers = []

        papers.extend(self.arxiv.fetch(query))

        papers.extend(self.semantic.search(query))

        return papers