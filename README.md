# Customer Architect Panel — Interview Briefing

> **Format:** 90-minute panel interview with 3–4 Elastic employees — **target 75 minutes of content** to leave time for a real conversation at the end
>
> **Structure:** Two parts — architectural strategy + hands-on Elastic Stack
>
> **Mindset:** Treat this as a **real customer interaction**, not an academic exercise. The panel is evaluating whether you'd be the architect they'd trust to walk into their own customer's boardroom. Anchor recommendations in facts, tailor your delivery to the audience, and **close every conversation with clear next steps**.

---

## Interview Structure

| Part | Topic | Target Duration |
|------|-------|----------|
| [Part 1 — Architecture Strategy](part-1/) | Cloud transformation design for a fictional enterprise client | ~35 min |
| Part 2 — Elastic Stack Exercise | Hands-on data ingestion and analysis *(pick one track below)* | ~35 min |
| Panel Q&A + wrap-up | Discussion, questions, feedback | ~20 min |

> ⏱️ **Time budget:** You have 90 minutes total. **Aim to deliver Parts 1 and 2 in ~70 minutes** — roughly 35 minutes each — so there's a full 20 minutes for conversation at the end. This is a panel, not a lecture.

### Choose One Track for Part 2

| Track | Folder |
|-------|--------|
| 📊 Observability | [part-2/observability/](part-2/observability/) |
| 🔍 Search & AI | [part-2/search/](part-2/search/) |
| 🛡️ Security Operations | [part-2/security/](part-2/security/) |
| ⚡ ESRally Benchmarking | [part-2/esrally/](part-2/esrally/) |

---

## Quick Start

1. Read this page in full
2. [Create an Elastic Cloud trial](https://cloud.elastic.co/) — save your `elastic` password and Cloud ID
3. Click through to [Part 1](part-1/) and your chosen Part 2 track
4. **Do your setup before the interview** — image pulls, model deployments, and API key configuration all take time

---

## Repo Contents

```
part-1/
├── README.md                          # Scenario brief, objectives, deliverable
├── ae-handoff.md                      # Internal AE prep notes
├── press-release.md                   # GOES public transformation announcement
├── discovery-call.md                  # Discovery session transcript
├── news-article.md                    # External coverage of the ticketing failure
├── diagrams/
│   └── goes-current-state-architecture.svg
└── presentations/
    └── goes-cloud-transformation-template.pptx

part-2/
├── observability/
│   ├── README.md                      # Host metrics, Apache log ingest, OTel Demo Shop
│   ├── sample-data/
│   │   └── apache_access.log.gz       # 2M-line Apache log, Apr 1–17 2026
│   ├── logstash/
│   │   └── pipeline.conf              # Logstash pipeline template
│   └── otel/
│       ├── collector-config.yml       # OTel Collector → Elastic Cloud config
│       └── docker-compose.override.yml
├── search/
│   ├── README.md                      # ELSER semantic search, RAG, Agent Builder
│   └── sample-data/
│       └── product-catalog.json       # 500-record e-commerce product catalogue
├── security/
│   └── README.md                      # Osquery, Security AI Assistant, Workflows
└── esrally/
    └── README.md                      # ESRally benchmarking against a remote cluster
```

---

## Elastic Cloud Setup

1. Go to [cloud.elastic.co](https://cloud.elastic.co/) and start a free 14-day trial
2. Create a new deployment — the defaults are fine
3. **Save immediately:** `elastic` user password and your **Cloud ID** (shown once on creation)
4. Your Cloud ID is visible later under **Deployment → Manage → Cloud ID**

> **Security track only:** You need a **Security-type Serverless project** (or a deployment with Elastic Security enabled) — this is separate from the standard deployment used in other exercises.

---

## General Notes

- **Target ~35 minutes per part** — roughly equal time for Part 1 and Part 2, leaving 20 minutes for panel Q&A and wrap-up
- **Close every part with next steps** — what follows this meeting? Workshops, POCs, deep-dives, timelines. Don't leave the panel wondering what happens Monday morning
- **Choose ONE exercise** for Part 2 — you will not have time for more than one in the 35-minute window
- **Within your exercise**, sections marked *Intermediate* and *Advanced* represent two levels of depth — your interviewer will indicate which is expected, or you may choose based on your background
- **Documentation may be imperfect** — working through ambiguity is part of what the panel is evaluating
- **Prepare in advance:** OTel Demo image pulls (~3 GB), ELSER model deployment (5–10 min), and LLM API key setup should all be done the day before your interview
- **Elastic Cloud trials expire after 14 days** — ensure your deployment is active the morning of your interview

---

*Impress us — The Elastic Team*
