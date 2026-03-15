from flask import Flask, render_template, request

from pipeline.ingestion_pipeline import PaperPipeline
from processing.cleaner import clean
from processing.embeddings import EmbeddingModel
from rag.vector_store import VectorStore
from analytics.summarizer import Summarizer

app = Flask(__name__)

pipeline = PaperPipeline()
embedder = EmbeddingModel()
summarizer = Summarizer()

vector_db = None
papers_cache = []


@app.route("/", methods=["GET", "POST"])
def index():

    global vector_db
    global papers_cache

    results = []

    if request.method == "POST":

        query = request.form["query"]

        papers = pipeline.run(query)

        papers_cache = papers

        texts = [clean(p.get("abstract","")) for p in papers]

        embeddings = embedder.encode(texts)

        dim = len(embeddings[0])

        vector_db = VectorStore(dim)

        vector_db.add(embeddings, texts)

        query_emb = embedder.encode([query])[0]

        similar_texts = vector_db.search(query_emb)

        for text in similar_texts:

            for p in papers_cache:

                if clean(p.get("abstract","")) == text:

                    summary = summarizer.summarize(text)

                    results.append({
                        "title": p.get("title"),
                        "summary": summary,
                        "source": p.get("source"),
                        "year": p.get("year","N/A"),
                        "link": p.get("link","")
                    })

    return render_template("index.html", results=results)

if __name__ == "__main__":
    print("Starting AI Research Assistant...")
    app.run(host="0.0.0.0", port=5000, debug=True)