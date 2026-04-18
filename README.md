# Panel Interview Briefing — Customer Architect Role

> **Format:** 90-minute panel interview with 3–4 Elastic employees
>
> **Structure:** Two parts — architectural strategy + hands-on Elastic Stack

## Repo Contents

| File | Description |
|------|-------------|
| [presentations/goes-cloud-transformation-template.pptx](presentations/goes-cloud-transformation-template.pptx) | Elastic-branded 4-slide PowerPoint template for Part 1 |
| [diagrams/goes-current-state-architecture.svg](diagrams/goes-current-state-architecture.svg) | GOES current-state on-premises architecture diagram |
| [sample-data/apache_access.log.gz](sample-data/apache_access.log.gz) | Apache access log — 2M lines, Apr 1–17 2026 (39 MB gzip → 427 MB uncompressed) |
| [sample-data/product-catalog.json](sample-data/product-catalog.json) | 500-record e-commerce product catalogue for the Search & AI exercise |
| [logstash/pipeline.conf](logstash/pipeline.conf) | Logstash pipeline template for the Apache log ingest step |
| [otel/collector-config.yml](otel/collector-config.yml) | OpenTelemetry Collector config routing telemetry to Elastic Cloud |
| [otel/docker-compose.override.yml](otel/docker-compose.override.yml) | Docker Compose override mounting the custom collector config |

## Quick Start

1. Read this briefing in full
2. [Create an Elastic Cloud trial](https://cloud.elastic.co/) — save your `elastic` password and Cloud ID
3. Choose **one exercise** from Exercises 1–4 for Part 2 of the panel
4. Prepare your Part 1 architecture diagrams separately (any diagramming tool is fine)
5. **Do your setup before the interview** — image pulls, model deployments, and API key configuration all take time

---

## Overview

| Part | Topic | Duration |
|------|-------|----------|
| Part 1 | Architecture Strategy for a Cloud Transformation | 30–45 min |
| Part 2 | Data Analysis and Ingestion Using Elastic Stack | 45 min |

---

## Part 1: Architectural Strategy for Cloud Transformation

### Scenario

- **Your Role:** Cloud Consultant
- **Client:** GOES — Global, Online E-Commerce and Streaming Content Provider
- **Current State:** On-premises (multiple physical data centers), self-managed
- **Strategic Direction:** Transitioning to a hybrid cloud environment

### Panel Stakeholders (Role-Play)

1. Application Stack Developer
2. Enterprise Architect
3. VP Engineering
4. Internal Business Stakeholder

### Objectives

Choose a cloud provider of your preference and guide the panel through the architectural transformation required.

- Design an architecture using **cloud-native patterns** that supports transitioning existing on-premise applications and infrastructure
- Address challenges of ensuring seamless operation in a **hybrid environment**
- Identify and discuss **potential risks** of moving to the cloud and propose mitigation strategies
- Highlight **opportunities** the cloud provides over their self-managed on-premise setup
- Demonstrate understanding of key transition considerations: **cost, security, scalability, and data management**

> **Note:** This segment does not require Elastic to be included. The focus is on your overall architectural understanding, migration strategy, and ability to identify risks and opportunities. Go both high-level and technically deep.

### Key Considerations

#### Size and Scale
Large multinational business with operations across multiple continents. Millions of active users generating substantial data daily.

#### Data Privacy and Compliance
Operates in regions with strict data privacy regulations (e.g., **GDPR in Europe**). Data storage and processing decisions must reflect these constraints.

#### Complexity of Services
Offers multiple services in parallel:
- Online shopping
- Content streaming
- Online payment processing

#### Peak Periods
Experiences significant traffic spikes (e.g., **Black Friday, Christmas**). Architecture must handle these loads without service disruption.

#### Business Continuity
High availability and resiliency are non-negotiable. Significant downtime directly translates to substantial revenue loss.

#### Innovation Mindset
Culture of frequent experimentation. Architecture must support **rapid changes and deployments**.

### Current State Architecture

![GOES Current State Architecture](diagrams/goes-current-state-architecture.svg)

### Deliverable

Prepare **diagrams** to visualize your architectural design.

> **Template:** Download the [Elastic-branded PowerPoint template](presentations/goes-cloud-transformation-template.pptx) — 4 pre-structured slides with Elastic branding ready to fill in.

These can represent:
- A step-by-step transformation process
- Various aspects of the final (target) architecture

---

## Part 2: Data Ingestion and Analysis Using Elastic Stack

### Objective

Use the Elastic platform to ingest and analyze a sample dataset — demonstrating hands-on capability and depth of curiosity about Elastic's products.

### Presentation Expectations

- Walk through your **process and findings**
- Explain your choices and the challenges encountered
- Discuss what your **visualizations and dashboards** reveal about the dataset
- Demonstrate the ability to gather data, search/filter it, and visualize results

---

## Exercises

### Prerequisites

**[Create an Elastic Cloud Trial](https://cloud.elastic.co/)**

1. Save the `elastic` user and its corresponding password
2. Once the instance is running, save your **Cloud ID**

---

### Exercise 1: Observability Stack Setup

#### Step 1 — Collect Host Metrics (Elastic Agent)

- Follow Elastic Agent instructions to collect metrics from your local machine
- **Disable log collection** for the system integration
- Navigate to **Observability → Infrastructure → Hosts** (may need to be enabled)

**Create 2 Alerts/Rules:**

| # | Condition | Notification |
|---|-----------|-------------|
| 1 | Average `system.cpu.system.pct` > 50% for last 1 min | Email alert |
| 2 | Average `system.memory.used.pct` > 85% for last 1 min | Email alert |

> **Bonus:** Customize the alert subject and body to include the metric name and current value

---

#### Step 2 — Ingest and Analyse Apache Logs (Logstash)

- Decompress the log file: `gunzip -k sample-data/apache_access.log.gz`
- Reference the [Logstash Quick Start Guide](https://www.elastic.co/guide/en/logstash/current/getting-started-with-logstash.html)
- Use **Logstash file input** and **Elasticsearch output** — see [logstash/pipeline.conf](logstash/pipeline.conf) for a starting template
- Apply a prebuilt Logstash grok pattern or define your own
- Create **Kibana visualizations** on points of interest from the Apache log
- Assemble visualizations into a **Kibana dashboard**

##### Analyse Logs with ES|QL

Once your Apache data is indexed into `apache-access-logs-*`, build a three-panel ES|QL dashboard:

**In Kibana → Dashboards → Create dashboard → Add panel → ES|QL**

1. **Top 10 Requested URLs** (horizontal bar chart):
   ```esql
   FROM apache-access-logs-*
   | STATS request_count = COUNT(*) BY request
   | SORT request_count DESC
   | LIMIT 10
   ```

2. **HTTP Status Code Distribution** (donut or pie):
   ```esql
   FROM apache-access-logs-*
   | STATS count = COUNT(*) BY response
   | SORT response ASC
   ```

3. **Request Volume by Hour** (line chart):
   ```esql
   FROM apache-access-logs-*
   | EVAL hour = DATE_TRUNC(1 hour, @timestamp)
   | STATS requests = COUNT(*) BY hour
   | SORT hour ASC
   ```

Save the dashboard as **"Apache Log Analysis — ES|QL"** and be prepared to walk through what each panel reveals.

> **Note on field names:** The `COMBINEDAPACHELOG` grok pattern produces `clientip`, `verb`, `request`, `response` (integer), and `bytes` (integer). Use these names in your ES|QL queries — they differ from ECS dot-notation.

> **Bonus:** Add a fourth panel showing the top 5 client IPs generating 4xx or 5xx errors:
> ```esql
> FROM apache-access-logs-*
> | WHERE response >= 400
> | STATS errors = COUNT(*) BY clientip
> | SORT errors DESC
> | LIMIT 5
> ```

> **Bonus:** Create a single-metric **anomaly detection job** to detect unusually high or low request rates (create a data view over `apache-access-logs-*` first if needed)

---

#### Step 3 — Observe with OpenTelemetry (OTel Demo Shop)

The monitored application is the **[OpenTelemetry Demo (Astronomy Shop)](https://github.com/open-telemetry/opentelemetry-demo)** — a realistic microservices e-commerce application with ~20 services written in Go, Java, Python, .NET, Node.js, Ruby, PHP, and Rust. It ships with full OpenTelemetry instrumentation and a built-in load generator, so traces, metrics, and logs flow continuously without any manual interaction.

**Data flow:**
```
Load Generator (Locust) → OTel Demo Services (~20)
                                    ↓
                        OpenTelemetry Collector
                                    ↓
                  Elastic Cloud  (APM · Metrics · Logs)
```

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Docker Compose v2)
- At least **6 GB RAM** allocated to Docker — check Settings → Resources before starting
- Your Elastic Cloud deployment running with APM endpoint and API key ready

**Steps:**

1. **Clone the demo** and check out a stable release:
   ```bash
   git clone https://github.com/open-telemetry/opentelemetry-demo.git
   cd opentelemetry-demo
   git checkout v1.12.0
   ```

2. **Copy the Elastic configuration files** from this repo:
   ```bash
   cp /path/to/customer-architect-panel/otel/collector-config.yml ./collector-config.yml
   cp /path/to/customer-architect-panel/otel/docker-compose.override.yml ./docker-compose.override.yml
   ```

3. **Edit `collector-config.yml`** — replace the two `REPLACE_WITH_YOUR_*` placeholders:
   - `endpoint` — find yours in Kibana under **Observability → Add data → APM → OpenTelemetry**
   - `Authorization` — create an API key in Kibana under **Stack Management → API Keys**, then encode it:
     ```bash
     echo -n "<id>:<secret>" | base64
     ```

4. **Start the stack** (first run pulls ~3 GB of images — do this before your interview):
   ```bash
   docker compose up --detach
   ```

5. **Verify telemetry is arriving** in Kibana:
   - **Observability → APM → Services** — ~15 services should appear (cartservice, checkoutservice, frontend, etc.)
   - **Observability → APM → Service Map** — live dependency graph across all services
   - **Dashboards** — search for *OpenTelemetry Demo* for a prebuilt overview

6. **Explore the running stack:**
   - Storefront UI: `http://localhost:8080`
   - Locust load generator: `http://localhost:8089`

7. **Stop when done:** `docker compose down`

> **Troubleshooting:** If services appear in APM but metrics are missing, check collector logs:
> `docker compose logs otelcol --tail 50` — a `401 Unauthorized` means your API key or endpoint needs correcting.
>
> **Override not working?** Copy the config directly as a fallback:
> `cp collector-config.yml src/otelcollector/otelcol-config.yml` then run `docker compose up` without the override file.

##### Explore OTel Metrics

1. Navigate to **Observability → APM → Services** → select `frontend` or `checkoutservice` → open the **Metrics** tab. Note which services expose runtime metrics (JVM heap, Go runtime) vs only request metrics.

2. Navigate to **Dashboards** → search *OpenTelemetry* → open the prebuilt dashboard. Identify the services with the highest request rate and highest p99 latency.

3. In **Kibana Lens**, build a custom panel:
   - Metric: `span.duration.us` at the 99th percentile
   - Breakdown by `service.name`
   - Time range: last 15 minutes

**Be prepared to explain the difference between infrastructure metrics and application/service metrics, and how both surface in Elastic Observability.**

> **Intermediate track — stop here.** Proceed to the Final Question.

##### Advanced: Correlate Logs and APM Traces

1. In **APM → Services**, find a service with a non-zero error rate (the load generator creates synthetic errors). Click into a failed transaction and open the **Logs** tab on the trace detail page.

2. Observe how Elastic links the APM trace to log lines via the shared `trace.id` field. From the trace detail, click through to **Discover** — Elastic pre-filters on `trace.id` to show only logs from that single request.

3. Navigate to **Observability → Logs → Explorer**, filter by `service.name: checkoutservice`, and use **Surrounding documents** around an error log line to reconstruct the sequence of events.

4. **Discuss:** How does correlating logs and traces across signal types reduce MTTR compared to siloed monitoring tools?

> **Bonus — Universal Profiling:** If your Elastic Cloud deployment includes Universal Profiling (available on some trial tiers), navigate to **Observability → Universal Profiling → Flamegraph** and observe CPU flame graphs — no additional agent configuration needed. Profiling shows *why* a service is slow; traces show *where*; metrics show *when*.

> **Bonus — Workflows:** Navigate to **Stack Management → Workflows** (or **Observability → Alerts → Manage Workflows** depending on your version). Create a workflow triggered by the CPU alert from Step 1 that: **(1)** captures the alert context, **(2)** runs an ES|QL query to surface the top processes at that moment, and **(3)** opens an Observability case with findings attached. Workflows use a visual trigger → condition → action builder — walk the panel through the automation you built and explain how it would reduce analyst toil in a production environment.

---

#### Final Question

> How are the vitals of your local host while ingesting data? Were any alerts triggered? If you explored the OTel metrics section — what differences did you observe between host-level infrastructure metrics and application service metrics?

---

### Exercise 2: Benchmark Elasticsearch with ESRally

- Benchmark against a **remote cluster** using ESRally
- Be prepared to explain:
  - Which **track(s)** you used
  - The **race results**

> **Bonus:** Create your own **[custom track](https://esrally.readthedocs.io/en/stable/adding_tracks.html)**

**Resources:**
- [ESRally Documentation](https://esrally.readthedocs.io/en/stable/)
- [ESRally GitHub Repository](https://github.com/elastic/rally)

---

### Exercise 3: Search and AI Retrieval

**Prerequisites:**
- Elastic Cloud trial deployment running
- Python 3.9+ installed locally
- At least **8 GB RAM** on your Elasticsearch deployment (the ELSER model loads in Elasticsearch — no local GPU needed)

The dataset for this exercise is **[sample-data/product-catalog.json](sample-data/product-catalog.json)** — 500 product records across 6 categories (footwear, apparel, electronics, camping, nutrition, accessories) with rich prose descriptions designed to demonstrate the advantage of semantic search over keyword matching.

---

#### Intermediate: Semantic Search with ELSER

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

#### Advanced: Retrieval-Augmented Generation (RAG)

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

#### Agent Builder

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

### Exercise 4: Security Operations

> ⚠️ **Prerequisite:** This exercise requires a **Security-type** Elastic Cloud Serverless project, or an existing deployment with the Elastic Security solution enabled. Set this up before your interview — it is separate from the standard Elasticsearch deployment used in other exercises.
>
> **macOS note:** Elastic Agent (and therefore Osquery) requires Full Disk Access. Grant it before your interview under **System Settings → Privacy & Security → Full Disk Access**.

---

#### Intermediate: Host Visibility with Osquery

1. **Add the Osquery Manager integration** to your existing Elastic Agent policy:
   Fleet → Agent policies → [your policy] → Add integration → search *Osquery Manager* → Add.

2. **Run a live query** from **Security → Investigations → Osquery → New live query**:

   macOS — installed applications:
   ```sql
   SELECT name, version, bundle_identifier FROM apps LIMIT 20
   ```
   Linux — installed packages:
   ```sql
   SELECT name, version FROM deb_packages LIMIT 20
   ```
   Windows — installed programs:
   ```sql
   SELECT name, version FROM programs LIMIT 20
   ```

3. **Run a threat-hunting query** — active network connections:
   ```sql
   SELECT pid, family, protocol, local_address, local_port,
          remote_address, remote_port, state
   FROM process_open_sockets
   WHERE state = 'ESTABLISHED'
   ```
   Walk the panel through each column. What would make a connection suspicious?

4. **Explore the data in Discover** — index `logs-osquery_manager.result-*`. Build a simple table visualisation showing installed application names and versions.

5. **Discuss:** What data does Osquery provide that a traditional metrics agent does not? What security use cases — asset inventory, vulnerability detection, incident response — does this enable?

> **Bonus:** Create a **scheduled Osquery pack** that runs the listening ports query every 5 minutes. Navigate to **Security → Investigations → Osquery → Packs** to configure continuous collection.

---

#### Advanced: Security AI Assistant

**Additional prerequisites:**
- An LLM connector configured in your Security project (same providers as Exercise 3)
- At least one security alert generated (see step 1 below)

1. **Generate a detection alert** — enable a prebuilt detection rule relevant to your OS:
   - **Security → Rules → Detection rules (SIEM) → Load Elastic prebuilt rules and enable them**
   - Enable *"Unusual Process for a macOS Host"* or *"Network Connection to Common Tunneling Port"*
   - Trigger it by running something detectable: `nmap localhost`, `curl https://ipinfo.io`, or similar
   - Wait 1–2 minutes for the alert to appear under **Security → Alerts**

2. **Open the AI Assistant from the alert:** In **Security → Alerts**, click on an alert → in the alert details panel, click the **AI Assistant** icon. The Assistant opens pre-loaded with the full alert context.

3. **Ask the assistant for triage context:**
   - *"What is this alert about and what is the potential business impact?"*
   - *"What investigation steps should I take for this type of alert?"*
   - *"What MITRE ATT&CK technique does this map to, and what are common next steps for an attacker?"*

4. **Invoke Osquery from within the AI Assistant:** Ask the assistant to run an Osquery query to investigate — e.g., *"Can you check what processes are currently listening on network ports on this host?"* The Assistant can call Osquery as an integrated tool from within the chat interface.

5. **Escalate to a case:** From the alert, click **Add to new case** → create a Security case. The AI Assistant conversation is automatically included in the case timeline. Show how this creates an auditable triage record.

6. **Discuss the value proposition:** How does the AI Assistant change the workflow for a Tier 1 SOC analyst? What are the risks — hallucination, over-reliance — and how does Elastic's grounding in the ELSER knowledge base and live Osquery data mitigate them?

> **Bonus — Custom system prompt:** Navigate to **Security → AI Assistant → Settings** and add a custom system prompt instructing the assistant to always cite the MITRE ATT&CK technique ID (e.g. T1059.001) in its responses. Show a before-and-after comparison of the assistant's answers.

> **Bonus — Automated Response with Workflows:** Navigate to **Security → Manage → Workflows** (or **Stack Management → Workflows**). Create an automated response workflow triggered when a high-severity alert fires. The workflow should: **(1)** enrich the alert by running a targeted Osquery query against the affected host, **(2)** pass the enriched context to the AI Assistant for an initial triage summary, and **(3)** automatically open a Security case with all findings attached. Walk the panel through the trigger → action chain you built and explain how this pattern scales SOC operations without adding headcount.

---

## General Notes

- **Choose ONE exercise** for Part 2 — you will not have time for more than one in the 45-minute window
- **Within your exercise**, sections marked *Intermediate* and *Advanced* represent two levels of depth — your interviewer will indicate which is expected, or you may choose based on your background
- **Time management is critical** — aim to complete the core steps and leave 5–10 minutes for discussion; bonuses are optional
- **Documentation may be imperfect** — working through ambiguity is part of what the panel is evaluating
- **Prepare in advance:** OTel Demo image pulls (~3 GB), ELSER model deployment (5–10 min), and LLM API key setup should all be done the day before your interview
- **Elastic Cloud trials expire after 14 days** — ensure your deployment is active the morning of your interview

---

*Impress us — The Elastic Team*
