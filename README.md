# Customer Architect Panel — Interview Briefing

> **Format:** 90-minute panel interview with 3–4 Elastic employees
>
> **Structure:** Two parts — architectural strategy + hands-on Elastic Stack

---

## Interview Structure

| Part | Topic | Duration |
|------|-------|----------|
| [Part 1 — Architecture Strategy](part-1-architecture.md) | Cloud transformation design for a fictional enterprise client | 30–45 min |
| Part 2 — Elastic Stack Exercise | Hands-on data ingestion and analysis *(pick one track below)* | 45 min |

### Choose One Track for Part 2

| Track | File |
|-------|------|
| 📊 Observability | [part-2-observability.md](part-2-observability.md) |
| 🔍 Search & AI | [part-2-search.md](part-2-search.md) |
| 🛡️ Security Operations | [part-2-security.md](part-2-security.md) |
| ⚡ ESRally Benchmarking | [part-2-esrally.md](part-2-esrally.md) |

---

## Quick Start

1. Read this page in full
2. [Create an Elastic Cloud trial](https://cloud.elastic.co/) — save your `elastic` password and Cloud ID
3. Click through to [Part 1](part-1-architecture.md) and your chosen Part 2 track
4. **Do your setup before the interview** — image pulls, model deployments, and API key configuration all take time

---

## Repo Contents

| File | Description |
|------|-------------|
| [part-1-architecture.md](part-1-architecture.md) | GOES scenario, stakeholders, objectives, current-state diagram |
| [part-2-observability.md](part-2-observability.md) | Host metrics, Apache log ingest, OTel Demo Shop |
| [part-2-search.md](part-2-search.md) | ELSER semantic search, RAG, AI Agent Builder |
| [part-2-security.md](part-2-security.md) | Osquery, Security AI Assistant, Automated Response |
| [part-2-esrally.md](part-2-esrally.md) | ESRally benchmarking against a remote cluster |
| [presentations/goes-cloud-transformation-template.pptx](presentations/goes-cloud-transformation-template.pptx) | Elastic-branded 4-slide PowerPoint template for Part 1 |
| [diagrams/goes-current-state-architecture.svg](diagrams/goes-current-state-architecture.svg) | GOES current-state on-premises architecture diagram |
| [sample-data/apache_access.log.gz](sample-data/apache_access.log.gz) | Apache access log — 2M lines, Apr 1–17 2026 (39 MB gzip) |
| [sample-data/product-catalog.json](sample-data/product-catalog.json) | 500-record e-commerce product catalogue for the Search & AI exercise |
| [logstash/pipeline.conf](logstash/pipeline.conf) | Logstash pipeline template for Apache log ingest |
| [otel/collector-config.yml](otel/collector-config.yml) | OpenTelemetry Collector config routing telemetry to Elastic Cloud |
| [otel/docker-compose.override.yml](otel/docker-compose.override.yml) | Docker Compose override for the OTel Demo Shop |

---

## Elastic Cloud Setup

1. Go to [cloud.elastic.co](https://cloud.elastic.co/) and start a free 14-day trial
2. Create a new deployment — the defaults are fine
3. **Save immediately:** `elastic` user password and your **Cloud ID** (shown once on creation)
4. Your Cloud ID is visible later under **Deployment → Manage → Cloud ID**

> **Security track only:** You need a **Security-type Serverless project** (or a deployment with Elastic Security enabled) — this is separate from the standard deployment used in other exercises.

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
