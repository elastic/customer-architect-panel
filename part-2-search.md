# Part 2 — Exercise 3: Search and AI Retrieval

> **Duration:** 45 minutes
>
> **Back to:** [Interview Briefing](README.md)

---

## Objective

Use Elastic's search and AI capabilities to build a semantic search experience over a product catalogue — then extend it into a retrieval-augmented generation (RAG) pipeline and an autonomous AI agent.

### What the Panel is Looking For

- Walk through your **process and findings**
- Explain your choices and the challenges you encountered
- Discuss what your **search results** reveal about the difference between keyword and semantic matching
- Demonstrate the ability to build and explain an AI-powered search architecture

---

## Prerequisites

- Elastic Cloud trial deployment running
- Python 3.9+ installed locally
- At least **8 GB RAM** on your Elasticsearch deployment (the ELSER model loads in Elasticsearch — no local GPU needed)

The dataset for this exercise is **[sample-data/product-catalog.json](sample-data/product-catalog.json)** — 500 product records across 6 categories (footwear, apparel, electronics, camping, nutrition, accessories) with rich prose descriptions designed to demonstrate the advantage of semantic search over keyword matching.

---

## Intermediate: Semantic Search with ELSER

1. **Index the catalogue with a keyword mapping** (your BM25 baseline):
   ```json
   PUT product-catalog-keyword
   {
     "mappings": {
       "properties": {
         "title":       { "type": "text" },
         "description": { "type": "text" },
         "category":    { "type": "keyword" }
       }
     }
   }
   ```
   Bulk-index `product-catalog.json` via Kibana Dev Tools or `curl`.

2. **Deploy ELSER** in Kibana → **Machine Learning → Trained Models** → find `.elser_model_2_linux-x86_64` → Deploy. Wait for status **Started** (~2–5 minutes on a trial deployment). If unavailable, use `e5-small-v2` as an alternative.

   > **Tip:** If the model cannot be deployed, upgrade the ML node to at least 2 GB in your deployment settings.

3. **Create a semantic index:**
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

4. **Reindex through the model** — Elasticsearch calls the inference endpoint automatically during indexing when `semantic_text` fields are present. Expect 3–10 minutes for 500 documents on a trial cluster.

5. **Compare results side by side.** Run both queries and discuss the difference:

   Keyword (BM25):
   ```json
   GET product-catalog-keyword/_search
   {
     "query": {
       "multi_match": {
         "query": "comfortable outdoor footwear for hiking",
         "fields": ["title", "description"]
       }
     }
   }
   ```

   Semantic:
   ```json
   GET product-catalog-semantic/_search
   {
     "query": {
       "semantic": {
         "field": "description",
         "query": "comfortable outdoor footwear for hiking"
       }
     }
   }
   ```

   Document 2–3 examples where semantic results are more relevant. Be ready to explain *why* — token matching vs embedding proximity in vector space.

> **Bonus:** Open **Search → Playground**, connect it to `product-catalog-semantic`, and use the Playground UI to test conversational search against your catalogue. Explain the Playground's role in validating a search experience before it reaches a production application.

---

## Advanced: Retrieval-Augmented Generation (RAG)

**Additional prerequisites:**
- An LLM API key for a provider supported by Kibana Connectors (OpenAI, Azure OpenAI, Amazon Bedrock, Google Gemini, etc.)
- Intermediate track completed (`product-catalog-semantic` index exists)

1. **Configure an LLM connector** in Kibana → **Stack Management → Connectors → Create connector** → select your LLM provider → enter your API key.

2. **Open Search → Playground** → select `product-catalog-semantic` → connect to the LLM connector you just created.

3. **Demonstrate grounded retrieval:**
   - Ask: *"What products do you carry for trail running?"*
   - Observe the **Context** panel — it shows which documents Elasticsearch retrieved before the LLM generated its response
   - Toggle off context and ask the same question — the LLM falls back to generic, ungrounded answers
   - The contrast illustrates the core value proposition of RAG

4. **Show the architecture:** Explain the three components — retriever (Elasticsearch semantic search), context builder (Playground / application layer), generator (LLM) — and how a customer would reproduce this using the Elasticsearch client and the `_search` + inference APIs.

5. Click **View code** in the Playground to show the Python or JavaScript equivalent. Walk through the request structure.

> **Bonus — Grounded RAG:** Set a custom system prompt that instructs the LLM to answer only using the retrieved context: *"If the answer is not contained in the provided context, say: I don't have that information."* Show how this prevents hallucination — the "grounded RAG" pattern used in production deployments.

---

## Agent Builder

Once you have semantic search working, use Elastic's **AI Agent Builder** to create an intelligent assistant that can autonomously decide when to query your product catalogue.

1. **Navigate to the Agent Builder** in Kibana → **Search → AI Search → Agents** (exact path varies by deployment version — search "Agent Builder" in the Kibana navigation if needed).

2. **Create a new agent** with a system prompt:
   > *You are a product search assistant for GOES, a global e-commerce company. When a customer asks about products, use the search tool to find relevant items from the catalogue and answer accurately based on those results. If no relevant products are found, say so clearly.*

3. **Add the product catalogue as a search tool:**
   - Tool name: `product_search`
   - Index: `product-catalog-semantic`
   - Description: *"Search the GOES product catalogue by description. Use this tool whenever the user asks about products, categories, or recommendations."*
   - Connect to the same LLM connector from the RAG step

4. **Test the agent with queries that require tool use:**
   - *"What waterproof options do you have for camping in the rain?"*
   - *"I need something for cold weather running — what do you recommend?"*
   - *"Do you have any nutrition products for endurance athletes?"*

   Observe the **agent reasoning loop**: the LLM decides to call `product_search`, receives results, then formulates a grounded response. This is the key difference from a static RAG pipeline — the agent has autonomy over *when* and *how many times* to call tools.

5. **Discuss the architecture:** How does an AI agent differ from a standard RAG pipeline? When would you use one over the other? What are the tradeoffs around latency, cost, and unpredictability?

> **Bonus:** Add a second tool — a static `get_category_list` tool that returns the six available product categories. Show how the agent uses multiple tools in a single conversation to answer a compound question like *"What categories do you carry, and what are your best electronics for outdoor use?"*

---

*← [Back to Interview Briefing](README.md)*
