# Part 2 — Exercise 1: Observability Stack Setup

> **Duration:** 45 minutes
>
> **Back to:** [Interview Briefing](README.md)

---

## Objective

Use the Elastic Observability platform to ingest and analyse data from multiple sources — demonstrating hands-on capability and depth of curiosity about Elastic's products.

### What the Panel is Looking For

- Walk through your **process and findings**
- Explain your choices and the challenges you encountered
- Discuss what your **visualizations and dashboards** reveal about the dataset
- Demonstrate the ability to gather data, search/filter it, and visualize results

---

## Step 1 — Collect Host Metrics (Elastic Agent)

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

## Step 2 — Ingest and Analyse Apache Logs (Logstash)

- Decompress the log file: `gunzip -k sample-data/apache_access.log.gz`
- Reference the [Logstash Quick Start Guide](https://www.elastic.co/guide/en/logstash/current/getting-started-with-logstash.html)
- Use **Logstash file input** and **Elasticsearch output** — see [logstash/pipeline.conf](logstash/pipeline.conf) for a starting template
- Apply a prebuilt Logstash grok pattern or define your own
- Create **Kibana visualizations** on points of interest from the Apache log
- Assemble visualizations into a **Kibana dashboard**

### Analyse Logs with ES|QL

Once your Apache data is indexed into `apache-access-logs-*`, use ES|QL to build a dashboard that tells a story about what the data reveals — **don't just visualise the data, demonstrate its value to a customer.**

**In Kibana → Dashboards → Create dashboard → Add panel → ES|QL**

Think about what a business stakeholder would care about when looking at web traffic logs:
- Where are users spending time, and where are they bouncing?
- When does demand spike, and is the platform keeping up?
- What does error behaviour reveal about reliability or potential threats?
- Which parts of the product — shopping, streaming, payments — are driving the most load?

Build a dashboard of at least 3 panels that answers questions like these. The panels below are **examples of the kind of analysis ES|QL enables** — use them as a starting point or inspiration, but the goal is a coherent narrative, not a checklist:

```esql
-- Request volume over time — is traffic behaving as expected?
FROM apache-access-logs-*
| EVAL hour = DATE_TRUNC(1 hour, @timestamp)
| STATS requests = COUNT(*) BY hour
| SORT hour ASC
```

```esql
-- Error rate by endpoint — where is the platform failing users?
FROM apache-access-logs-*
| WHERE response >= 400
| STATS errors = COUNT(*) BY request
| SORT errors DESC
| LIMIT 10
```

```esql
-- Bandwidth by content type — what is driving egress cost?
FROM apache-access-logs-*
| STATS total_bytes = SUM(bytes) BY verb
| SORT total_bytes DESC
```

> **Note on field names:** The `COMBINEDAPACHELOG` grok pattern produces `clientip`, `verb`, `request`, `response` (integer), and `bytes` (integer). Use these names in your ES|QL queries — they differ from ECS dot-notation.

Be prepared to walk the panel through your dashboard and explain: *what would you tell a customer's VP of Engineering or Head of E-Commerce based on what you see here?*

> **Bonus:** Create a single-metric **anomaly detection job** to detect unusually high or low request rates (create a data view over `apache-access-logs-*` first if needed)

---

## Step 3 — Observe with OpenTelemetry (OTel Demo Shop)

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

### Explore OTel Metrics

1. Navigate to **Observability → APM → Services** → select `frontend` or `checkoutservice` → open the **Metrics** tab. Note which services expose runtime metrics (JVM heap, Go runtime) vs only request metrics.

2. Navigate to **Dashboards** → search *OpenTelemetry* → open the prebuilt dashboard. Identify the services with the highest request rate and highest p99 latency.

3. In **Kibana Lens**, build a custom panel:
   - Metric: `span.duration.us` at the 99th percentile
   - Breakdown by `service.name`
   - Time range: last 15 minutes

**Be prepared to explain the difference between infrastructure metrics and application/service metrics, and how both surface in Elastic Observability.**

> **Intermediate track — stop here.** Proceed to the Final Question.

### Advanced: Correlate Logs and APM Traces

1. In **APM → Services**, find a service with a non-zero error rate (the load generator creates synthetic errors). Click into a failed transaction and open the **Logs** tab on the trace detail page.

2. Observe how Elastic links the APM trace to log lines via the shared `trace.id` field. From the trace detail, click through to **Discover** — Elastic pre-filters on `trace.id` to show only logs from that single request.

3. Navigate to **Observability → Logs → Explorer**, filter by `service.name: checkoutservice`, and use **Surrounding documents** around an error log line to reconstruct the sequence of events.

4. **Discuss:** How does correlating logs and traces across signal types reduce MTTR compared to siloed monitoring tools?

> **Bonus — Universal Profiling:** If your Elastic Cloud deployment includes Universal Profiling (available on some trial tiers), navigate to **Observability → Universal Profiling → Flamegraph** and observe CPU flame graphs — no additional agent configuration needed. Profiling shows *why* a service is slow; traces show *where*; metrics show *when*.

> **Bonus — Workflows:** Navigate to **Stack Management → Workflows** (or **Observability → Alerts → Manage Workflows** depending on your version). Create a workflow triggered by the CPU alert from Step 1 that: **(1)** captures the alert context, **(2)** runs an ES|QL query to surface the top processes at that moment, and **(3)** opens an Observability case with findings attached. Workflows use a visual trigger → condition → action builder — walk the panel through the automation you built and explain how it would reduce analyst toil in a production environment.

---

## Final Question

> How are the vitals of your local host while ingesting data? Were any alerts triggered? If you explored the OTel metrics section — what differences did you observe between host-level infrastructure metrics and application service metrics?

---

*← [Back to Interview Briefing](README.md)*
