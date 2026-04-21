# Part 2 — Exercise 4: Security Operations

> **Duration:** 45 minutes
>
> **Back to:** [Interview Briefing](../../README.md)

---

## Objective

Use the Elastic Security platform to demonstrate host visibility, threat investigation, and AI-assisted triage — then extend it into an automated response workflow.

### What the Panel is Looking For

- Walk through your **process and findings**
- Explain your choices and the challenges you encountered
- Discuss what your **queries and detections** reveal about the environment
- Demonstrate the ability to investigate, escalate, and automate security workflows

---

## Prerequisites

> ⚠️ This exercise requires a **Security-type** Elastic Cloud Serverless project, or an existing deployment with the Elastic Security solution enabled. Set this up before your interview — it is separate from the standard Elasticsearch deployment used in other exercises.
>
> **macOS note:** Elastic Agent (and therefore Osquery) requires Full Disk Access. Grant it before your interview under **System Settings → Privacy & Security → Full Disk Access**.

---

## Intermediate: Host Visibility with Osquery

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

## Advanced: Security AI Assistant

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

*← [Back to Interview Briefing](../../README.md)*
