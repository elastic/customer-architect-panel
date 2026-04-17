# Panel Interview Briefing — Customer Architect Role

> **Format:** 90-minute panel interview with 3–4 Elastic employees
>
> **Structure:** Two parts — architectural strategy + hands-on Elastic Stack

## Repo Contents

| File | Description |
|------|-------------|
| [presentations/goes-cloud-transformation-template.pptx](presentations/goes-cloud-transformation-template.pptx) | Elastic-branded 4-slide PowerPoint template for Part 1 |
| [diagrams/goes-current-state-architecture.svg](diagrams/goes-current-state-architecture.svg) | GOES current-state on-premises architecture diagram |
| [sample-data/apache_access.log.gz](sample-data/apache_access.log.gz) | Apache access log file used in Exercise 1 — 2M lines, Apr 1–17 2026 (gzip compressed, 39 MB → 427 MB uncompressed) |
| [logstash/pipeline.conf](logstash/pipeline.conf) | Logstash pipeline configuration template for Exercise 1 |

## Quick Start

1. Read this briefing in full
2. [Create an Elastic Cloud trial](https://cloud.elastic.co/) and save your credentials + Cloud ID
3. Choose Exercise 1 or Exercise 2 for Part 2 of the panel
4. Prepare your Part 1 architecture diagrams separately (any diagramming tool is fine)

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

#### Collect Metrics via System Integration (Elastic Agent)

- Follow Elastic Agent instructions to collect metrics from your local machine
- **Disable log collection** for the system integration
- Navigate to **Observability → Infrastructure → Hosts** (may need to be enabled)

**Create 2 Alerts/Rules:**

| # | Condition | Notification |
|---|-----------|-------------|
| 1 | Average `system.cpu.system.pct` > 50% for last 1 min | Email alert |
| 2 | Average `system.memory.used.pct` > 85% for last 1 min | Email alert |

> **Bonus:** Customize alert subject and content

---

#### Collect Logs via Logstash

- Use the provided **[Apache access log file](sample-data/apache_access.log.gz)** in this repo (gunzip before use: `gunzip -k sample-data/apache_access.log.gz`)
- Reference the [Logstash Quick Start Guide](https://www.elastic.co/guide/en/logstash/current/getting-started-with-logstash.html)
- Use **Logstash file input** and **Elasticsearch output** — see [pipeline.conf](logstash/pipeline.conf) for a starting template
- Apply a prebuilt Logstash grok pattern or define your own
- Create **Kibana visualizations** on points of interest from the Apache log
- Assemble visualizations into a **Kibana dashboard**

> **Bonus:** Create a single-metric **anomaly detection job** to detect excessive high or low log rate (create a data view first if needed)

---

#### Collect APM Traces (Spring Pet Clinic)

The monitored application is **Spring Pet Clinic** (Java).

**Prerequisites:**
- JDK 17
- `JAVA_HOME` set

**Steps:**
1. Follow instructions in the [Spring Pet Clinic repo](https://github.com/spring-projects/spring-petclinic) to run the application
2. Set up **Elastic APM** using the APM Agents tab in Kibana (detailed per-language instructions available there)
3. Instrument using the **Java APM agent**
4. Verify in **Observability → APM → Services**

---

#### Final Question

> How are the vitals of your local host while ingesting data? Were any alerts triggered?

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

## General Notes

- **Time management** is nearly as important as content — be mindful of scope within the 90-minute window
- Documentation referenced in exercises may not be perfect — work through it
- Choose **either Exercise 1 or Exercise 2** for Part 2

---

*Impress us — The Elastic Team*
