# Part 2 — Exercise 2: Benchmark Elasticsearch with ESRally

> **Duration:** 45 minutes
>
> **Back to:** [Interview Briefing](../../README.md)

---

## Objective

Use ESRally to benchmark an Elasticsearch cluster — demonstrating understanding of performance testing methodology and the ability to interpret and communicate results.

### What the Panel is Looking For

- Walk through your **process and findings**
- Explain which tracks you chose and why
- Interpret the **race results** — what do the metrics tell you about cluster performance?
- Discuss what you would do differently to optimise the cluster based on your findings

---

## Prerequisites

- Elastic Cloud trial deployment running — save your Cloud ID and `elastic` user credentials
- Python 3.8+ and pip installed locally
- ESRally installed: `pip install esrally`

---

## Exercise

### Step 1 — Benchmark Against Your Remote Cluster

Run ESRally against your Elastic Cloud deployment using a standard track:

```bash
esrally race \
  --track=geonames \
  --target-hosts=<your-cloud-endpoint>:9243 \
  --client-options="use_ssl:true,verify_certs:true,basic_auth_user:'elastic',basic_auth_password:'<your-password>'" \
  --pipeline=benchmark-only \
  --report-format=csv \
  --report-file=results.csv
```

> **Find your endpoint:** Kibana → Deployment → Manage → Copy endpoint (strip the trailing `/`)

### Step 2 — Review Race Results

After the race completes, ESRally prints a summary table. Key metrics to understand and discuss:

| Metric | What it means |
|--------|--------------|
| `indexing_throughput` | Documents indexed per second |
| `service_time` (p50/p90/p99) | How long operations actually take |
| `latency` (p50/p90/p99) | Time from request submission to response |
| `error_rate` | Percentage of operations that failed |
| `merge_time` | Time Elasticsearch spent merging Lucene segments |

Be ready to explain: *What would you tell a customer's infrastructure team based on these numbers?*

### Step 3 — Try a Second Track (Optional)

ESRally ships with many tracks covering different workloads. Try a second one and compare:

| Track | Workload type |
|-------|--------------|
| `geonames` | Geo queries on place names |
| `http_logs` | Log ingestion and search |
| `nyc_taxis` | Time-series analytics |
| `so` | Stack Overflow Q&A dataset |

```bash
esrally list tracks
```

---

## Discussion Points

Be prepared to discuss:

- **Which track(s)** you used and why they're relevant to a real-world workload
- **What the results reveal** about the cluster's throughput, latency profile, and capacity limits
- **How you would use ESRally** in a customer engagement — when would you reach for it, and what decisions would the results inform?
- **Tradeoffs** between different shard configurations, refresh intervals, and replica counts

---

## Resources

- [ESRally Documentation](https://esrally.readthedocs.io/en/stable/)
- [ESRally GitHub Repository](https://github.com/elastic/rally)
- [Adding Custom Tracks](https://esrally.readthedocs.io/en/stable/adding_tracks.html)

> **Bonus:** Create your own **[custom track](https://esrally.readthedocs.io/en/stable/adding_tracks.html)** using a dataset relevant to a customer workload you've encountered. Walk the panel through how you designed the operations and what you were trying to measure.

---

*← [Back to Interview Briefing](../../README.md)*
