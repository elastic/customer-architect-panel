# Part 2 — Exercise 1: Observability (Elastic Serverless + OpenTelemetry)

> **Duration:** 45 minutes
>
> **Back to:** [Interview Briefing](../../README.md)

---

## Objective

Stand up **Elastic Observability Serverless (Complete)**, send **OTLP** metrics, traces, and logs from the **OpenTelemetry Demo** running on **local Kubernetes**, then walk the panel through the **Serverless Observability project UI** — every major left-nav experience — and explain what a customer would get from each.

This exercise is intentionally **OpenTelemetry-first**. Elastic is a major contributor to the OTel ecosystem; candidates should demonstrate comfort with OTLP and curated Observability experiences, not legacy one-off log shipping.

### What the Panel is Looking For

- A clear path from **signup → project → telemetry → insight**
- Comfort with **OTLP** (logs, metrics, and traces) into Elastic
- Ability to **navigate Observability Complete** and explain customer value per area
- Process, tradeoffs, and findings — not just “I clicked until something lit up”

---

## Architecture

```
Local Kubernetes (kind / minikube / Docker Desktop K8s)
        │
        │  OpenTelemetry Demo (Astronomy Shop) via Helm
        │  ~20 instrumented microservices + load generator
        ▼
OpenTelemetry Collector (in-cluster)
        │  OTLP (traces · metrics · logs)
        ▼
Elastic Cloud — Observability Serverless project (Complete)
        │
        ▼
Kibana Observability UI (Services, Logs, Infrastructure, SLOs, Alerts, …)
```

---

## Step 1 — Create an Elastic Observability Serverless project

1. Sign up / log in at [cloud.elastic.co](https://cloud.elastic.co/)
2. Create a new **Observability** project on **Elastic Cloud Serverless**
3. Choose the **Complete** feature tier (full-stack experiences: logs, metrics, traces, SLOs, curated UIs, AI assists where available)
4. Open the project in Kibana and keep it handy — you will walk the **left navigation** in Step 4

### Get your OTLP endpoint and API key

In the project, open **Add data → OpenTelemetry** (or **Observability → Add data → APM / OpenTelemetry** depending on UI version) and note:

| Value | Where it goes |
|---|---|
| **Managed OTLP / APM OTLP endpoint** | `my-values-file.yaml` → exporter `endpoint` |
| **API key** | `Authorization: ApiKey <key>` header |

> **Tip:** Prefer the **Managed OTLP Endpoint** path when the UI offers it for Serverless — native OTLP in, Elastic handles scaling and signal processing.

---

## Step 2 — Local Kubernetes + OpenTelemetry Demo (Helm)

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) **or** another local Kubernetes (kind / minikube / k3d)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm 3](https://helm.sh/docs/intro/install/)
- At least **8 GB RAM** available to the cluster (OTel Demo is not tiny)

Enable Kubernetes in Docker Desktop (**Settings → Kubernetes → Enable**) *or* create a kind cluster:

```bash
kind create cluster --name otel-demo
```

### Install the OpenTelemetry Demo

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update open-telemetry
```

Copy the values cheat sheet from this repo and edit the two placeholders:

```bash
cp /path/to/customer-architect-panel/part-2/observability/otel/my-values-file.yaml ./my-values-file.yaml
# Edit REPLACE_WITH_YOUR_OTLP_ENDPOINT and REPLACE_WITH_YOUR_API_KEY
```

Install:

```bash
helm install my-otel-demo open-telemetry/opentelemetry-demo \
  --values my-values-file.yaml \
  --namespace otel-demo \
  --create-namespace
```

Watch pods come up:

```bash
kubectl get pods -n otel-demo -w
```

### Verify the storefront (optional)

```bash
kubectl port-forward -n otel-demo svc/my-otel-demo-frontend-proxy 8080:8080
```

Open `http://localhost:8080` — generate a little traffic while the load generator runs.

### Uninstall when done

```bash
helm uninstall my-otel-demo -n otel-demo
# kind delete cluster --name otel-demo   # if you used kind
```

> **Troubleshooting**
> - Collector `401` / auth errors → API key or endpoint wrong in `my-values-file.yaml`
> - No services in Elastic after 5–10 minutes → `kubectl logs -n otel-demo deploy/my-otel-demo-otelcol --tail=80`
> - Cluster OOMs → raise Docker Desktop memory or disable optional demo components in values
>
> **Arrays replace on Helm merge:** if you override the Collector `traces` exporters, keep `spanmetrics` in that list (required by the chart). Our sample values file already does this.

---

## Step 3 — Confirm telemetry in Elastic

Within a few minutes you should see:

| Check | Where |
|---|---|
| Services appear | **Observability → APM / Services** (frontend, checkout, cart, …) |
| Traces / dependencies | Service map / trace waterfall |
| Logs correlated | Logs experiences filtered by `service.name` / `trace.id` |
| Metrics flowing | Service metrics + infrastructure / host-adjacent views as available |

Be ready to explain the difference between **infrastructure** signals and **application** signals (services, transactions, spans) and how OTLP carries all three signal types.

---

## Step 4 — Showcase the Serverless Observability project (left nav)

**This is the core of the exercise.** Open your Observability Complete project and walk the panel through **each major left-nav area**. For every section, say out loud:

1. **What it is**  
2. **What customer problem it solves**  
3. **What you see from the OTel Demo right now**

Use this checklist (names may vary slightly by UI version — cover the intent of each):

| Left-nav area | What to show / discuss |
|---|---|
| **Overview / Home** | Fleet health of the estate at a glance — what a VP Eng would open first |
| **Services / APM** | Service inventory, latency, errors, throughput from Astronomy Shop |
| **Traces / Service map** | Dependencies; pick a slow or failing transaction and walk the waterfall |
| **Logs** | Service logs; jump from a trace → related logs via `trace.id` |
| **Infrastructure / Hosts / K8s** | Cluster / container / host context next to app signals |
| **SLOs** | Define or discuss an SLO on a critical service (e.g. frontend availability / latency) |
| **Alerts / Cases** | One meaningful alert (error rate or latency); how it would page a human |
| **Dashboards** | OTel / curated dashboards — narrative, not wallpaper |
| **AI Assistant** (if available on Complete) | Ask a grounded question about a failing service / spike |
| **Add data / Integrations** | How a customer expands beyond this demo (more K8s, cloud, synthetics) |

> **Rubric:** Candidates who only open Services and stop will under-index. Candidates who connect **signal → investigation → customer outcome** across the nav will stand out.

### Suggested investigation story (5 minutes)

1. Find a service with elevated latency or errors  
2. Open a trace → identify the slow dependency  
3. Jump to related logs  
4. Discuss whether you’d alert, create an SLO, or open a case  
5. Tie it back to what you’d tell a customer’s platform owner tomorrow morning  

---

## Step 5 — Optional stretch

Pick **one** if time remains:

- **SLO:** Create an SLO on `frontend` (or checkout) latency/availability and explain burn-rate alerting  
- **Alert:** Error-rate or latency threshold on a hot service, with a clear notification path  
- **ES\|QL:** One panel that answers a business question from OTel logs/metrics (not vanity charts)  
- **Workflows:** Alert → enrich with a query → open a case (where available)

---

## Final Question

> Walk us through your Observability Complete project. For two left-nav areas of your choice, what customer value did you demonstrate with the OTel Demo data — and what would you do next if this were a real Azure/AWS Kubernetes estate?

---

## Appendix A — Docker Compose alternative (no Kubernetes)

If you cannot run local Kubernetes, you may use Docker Compose with the files under [`otel/`](otel/):

1. Clone [opentelemetry-demo](https://github.com/open-telemetry/opentelemetry-demo) and check out a stable tag  
2. Copy `otel/collector-config.yml` and `otel/docker-compose.override.yml` into the demo root  
3. Fill in endpoint + API key placeholders  
4. `docker compose up --detach`  

Kubernetes + Helm remains the **preferred** path for this exercise.

---

## Appendix B — Legacy Logstash lab (not required)

The previous Apache + Logstash lab files remain under [`logstash/`](logstash/) and [`sample-data/`](sample-data/) for reference only. **Do not use them for the panel exercise** unless a facilitator explicitly asks. Prefer OTLP.

---

*← [Back to Interview Briefing](../../README.md)*
