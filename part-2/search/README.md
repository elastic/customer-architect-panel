# Part 2 — Exercise 3: Search and AI Retrieval

> **Duration:** 45 minutes
>
> **Back to:** [Interview Briefing](../../README.md)

---

## Objective

Build a working search application and AI chatbot powered by Elastic — demonstrating how semantic and hybrid search, retrieval-augmented generation, and a real frontend come together into a production-grade search experience.

### What the Panel is Looking For

- Walk through your **architecture and implementation choices**
- Explain the difference between BM25, semantic, and hybrid search — and when each wins
- Demonstrate a **live chatbot or search UI** grounded in your chosen dataset
- Discuss how you would take this to a customer

---

## Prerequisites

- Elastic Cloud trial deployment running
- Python 3.9+ and `pip` installed
- Node.js 18+ and `yarn` installed (for the frontend)
- An LLM API key (OpenAI, Azure OpenAI, Amazon Bedrock, Google Gemini, or any Langchain-supported provider)
- At least **8 GB RAM** on your Elasticsearch deployment (ELSER loads in Elasticsearch — no local GPU needed)

---

## Choose Your Dataset

Pick one of the following — you'll use it for both the search and chatbot steps:

| Option | Description |
|--------|-------------|
| **A — Product Catalogue** | Use the provided [`sample-data/product-catalog.json`](sample-data/product-catalog.json) — 500 e-commerce product records with rich prose descriptions across 6 categories |
| **B — Crawl a Website** | Use the [Elastic Web Crawler](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors-web-crawler.html) (available in Kibana → Search → Connectors) to crawl a public site of your choosing — a docs site, blog, or product catalogue works well |

> **Tip on Option B:** The web crawler runs inside Kibana and populates an index automatically. Pick a site with rich text content (not heavy JavaScript-rendered SPAs) for best results. Allow 10–15 minutes for crawling before the next steps.

---

## Step 1 — Ingest and Index with ELSER

### Option A — Product Catalogue

1. **Deploy ELSER** — Kibana → **Machine Learning → Trained Models** → find `.elser_model_2_linux-x86_64` → Deploy. Wait for status **Started** (~2–5 min). Use `e5-small-v2` as an alternative if unavailable.

   > **Tip:** If the model cannot be deployed, upgrade the ML node to at least 2 GB in your deployment settings.

2. **Create an index with a semantic mapping:**
   ```json
   PUT product-catalog-semantic
   {
     "mappings": {
       "properties": {
         "title":       { "type": "text" },
         "description": {
           "type": "semantic_text",
           "inference_id": ".elser-2-elasticsearch"
         },
         "category":    { "type": "keyword" }
       }
     }
   }
   ```

3. **Bulk-index the catalogue** via Kibana Dev Tools or `curl`. Elasticsearch automatically generates sparse embeddings via the `semantic_text` inference pipeline. Expect 3–10 minutes for 500 documents on a trial cluster.

### Option B — Web Crawler

1. In Kibana → **Search → Connectors → Web Crawler** → create a new crawler, enter your target domain, and start a crawl.
2. The crawler creates an index automatically. Once crawling is complete, verify documents in **Discover**.
3. **Add a semantic field** to the body/content field by creating a new index with `semantic_text` and reindexing:
   ```json
   POST _reindex
   {
     "source": { "index": "your-crawler-index" },
     "dest":   { "index": "your-semantic-index" }
   }
   ```

---

## Step 2 — Build a Hybrid Search Experience

With your data indexed, build a search experience that combines BM25 keyword matching with ELSER semantic search using **Reciprocal Rank Fusion (RRF)**.

### Run a Hybrid Query

```json
GET product-catalog-semantic/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": {
              "multi_match": {
                "query": "lightweight gear for wet weather",
                "fields": ["title", "description"]
              }
            }
          }
        },
        {
          "standard": {
            "query": {
              "semantic": {
                "field": "description",
                "query": "lightweight gear for wet weather"
              }
            }
          }
        }
      ]
    }
  }
}
```

**Compare the three approaches side by side** — run the same query as pure BM25, pure semantic, and hybrid RRF. Document 2–3 examples where hybrid outperforms either approach alone. Be ready to explain *why* — complementary signals, long-tail intent, vocabulary mismatch.

> **Reference:** The [Search Tutorial on Elastic Search Labs](https://www.elastic.co/search-labs/tutorials/search-tutorial/welcome) walks through building a full Flask + Python search app with BM25, vector search, semantic search, and RRF hybrid ranking — use it as a guide for your frontend in Step 3.

---

## Step 3 — Build a Frontend

Build a simple working UI that demonstrates your search experience. This doesn't need to be polished — it needs to be **functional and explainable**.

**Primary resource:** Follow the [Elastic Search Labs Chatbot Tutorial](https://www.elastic.co/search-labs/tutorials/chatbot-tutorial/welcome) — it provides a complete Flask + React/TypeScript starter app with Elasticsearch and Langchain wiring already done. Adapt it to your dataset.

```bash
# Clone the tutorial's starter app
git clone https://github.com/elastic/elasticsearch-labs
cd elasticsearch-labs/examples/chatbot-rag-app
```

### What to Build

Choose one (or both if time allows):

| UI Type | Description |
|---------|-------------|
| **Search interface** | Search box + results list — queries your hybrid index, shows ranked results with title, snippet, and category/source |
| **Chatbot** | Conversational interface — uses RAG to answer questions grounded in your indexed content, with source citations |

> **Playground is a validation tool, not the deliverable.** Use Kibana → **Search → Playground** to verify your index and prompts work before wiring them into your frontend — but the panel wants to see a real application, not the Playground UI.

### Minimum Viable Backend (Python/Flask)

```python
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch(cloud_id="YOUR_CLOUD_ID", basic_auth=("elastic", "YOUR_PASSWORD"))

@app.route("/search")
def search():
    q = request.args.get("q", "")
    resp = es.search(index="product-catalog-semantic", body={
        "retriever": {
            "rrf": {
                "retrievers": [
                    {"standard": {"query": {"multi_match": {"query": q, "fields": ["title", "description"]}}}},
                    {"standard": {"query": {"semantic": {"field": "description", "query": q}}}}
                ]
            }
        }
    })
    hits = [{"title": h["_source"]["title"], "description": h["_source"]["description"]} for h in resp["hits"]["hits"]]
    return jsonify(hits)

if __name__ == "__main__":
    app.run(debug=True)
```

### Adding the Chatbot Layer

To extend your search app into a RAG chatbot, the [Chatbot Tutorial](https://www.elastic.co/search-labs/tutorials/chatbot-tutorial/welcome) covers:

1. **LLM connector** — add your API key via environment variable (`python-dotenv`)
2. **Langchain RAG chain** — retrieves from Elasticsearch, passes context to the LLM, returns grounded answers
3. **Chat history** — maintaining multi-turn conversation context across exchanges
4. **React/TypeScript frontend** — the starter repo includes a chat UI ready to connect to your Flask backend

---

## Step 4 — Demo and Discussion

Walk the panel through a **live demo** of your running application. Cover:

1. **Architecture walkthrough** — how does a query flow from the UI through Elasticsearch to the LLM and back?
2. **Hybrid vs keyword vs semantic** — show a query where hybrid wins and explain why
3. **Grounding** — show what happens when the LLM is asked something not in your index (it should say so)
4. **Production path** — how would a customer deploy this? What would you change before it goes live?

---

## Resources

- [Elastic Search Labs](https://www.elastic.co/search-labs)
- [Chatbot Tutorial](https://www.elastic.co/search-labs/tutorials/chatbot-tutorial/welcome) — Flask + React RAG chatbot starter
- [Search Tutorial](https://www.elastic.co/search-labs/tutorials/search-tutorial/welcome) — BM25 → vector → semantic → hybrid RRF walkthrough
- [Elasticsearch Python client](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)
- [Web Crawler docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors-web-crawler.html)

---

*← [Back to Interview Briefing](../../README.md)*
