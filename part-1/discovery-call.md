# GOES — Discovery Call Transcript

**Date:** 8 April 2026
**Duration:** ~55 minutes
**Format:** Video call

**Participants:**
- **Consultant** *(us)*
- **Marcus Webb** — Chief Technology Officer, GOES
- **David Yuen** — Enterprise Architect, GOES
- **Priya Sharma** — VP Engineering, GOES
- **Tom Riordan** — Head of E-Commerce Technology, GOES

*Note: Lightly edited for clarity. Some crosstalk removed.*

---

**Consultant:** Marcus, thanks for making this happen — we've been looking forward to a broader conversation. Maybe a good place to start is you setting the context. What does this transformation mean to you, and what does success look like in three years?

**Marcus Webb:** Sure. Look, the short version is that we are operationally constrained in a way that is becoming competitively dangerous. We've built something impressive — 45 million active users, live events, payments, global e-commerce — but it's sitting on an infrastructure that was designed in 2006. We have two data centres, a lot of metal, and a quarterly release cycle. That's not a technology company by today's standards.

Success in three years is us having the ability to ship weekly, scale on demand, and stop writing cheques for hardware we use four days a year.

**Consultant:** When you say four days a year — can you say more about what peak looks like for you?

**Marcus Webb:** Tom, you want to take that?

**Tom Riordan:** Yeah. Black Friday weekend is the obvious one — we see roughly four to five times our normal request volume over about 72 hours. But honestly the harder pattern now is on-sales. When we open ticket sales for a major tour, we can have two million people hitting a single SKU inside of 90 seconds. That's a different kind of problem than seasonal e-commerce load. We don't have a great answer for it today.

**Consultant:** Is that the pattern that caused the January incident?

**Tom Riordan:** Yes. We got caught flat. We knew the on-sale was coming, we'd done some capacity planning, but the actual traffic shape was different than what we modelled. We queued fine up to about the first 400,000 requests and then the checkout layer started refusing connections. We had to pull the sale and reschedule.

**Priya Sharma:** Which was its own kind of pain. Re-announcing a cancelled on-sale to a fan base that's already angry is not a great experience.

**Consultant:** David, how are you thinking about the architecture for something like that — the on-sale spike — today versus where you'd want to get to?

**David Yuen:** Today it's manual. We provision ahead of known peaks. We're pretty good at that for predictable events like Black Friday because we've done it many times. The ticketing spikes are harder because the demand is both sudden and clustered on a very small number of SKUs. You can't really pre-scale for that without massively overprovisioning the rest of the time.

Where I'd want to get to is some combination of proper queue-based architecture in front of inventory and checkout, with auto-scaling compute behind it. That part I don't think is controversial. Where I have more questions is about the platform decisions around that — which services, which providers, what the operational model looks like in five years if the business changes.

**Consultant:** That's a useful distinction. Can you say more about the questions you have on the platform side?

**David Yuen:** Sure. We've been through a few of these evaluations over the years. My concern is always the same: we make a set of architectural commitments, we build deep integrations, and then we're dependent on a set of pricing and product decisions that we don't control. I'd want any architecture to have clear answers on what the exit path looks like if the relationship changes.

**Marcus Webb:** David and I have had this conversation. I understand the concern but I think the risk of staying where we are outweighs the risk of making a platform commitment. The question for me is which commitment to make and how to structure it.

**Priya Sharma:** I'd add — the operational model is also important for me. We have about 80 people in SRE and platform. Whatever we build has to be manageable by that team. We can't assume we're going to double the headcount to run the new architecture.

**Consultant:** That's a really important constraint. Is there a number attached to that — in terms of how much manual operational overhead you're carrying today that you'd want to reduce?

**Priya Sharma:** I don't have an exact number in front of me. Roughly speaking, I'd say 30 to 40 percent of our platform engineering time is on infrastructure maintenance rather than product enablement. That's the rough shape of it. Tom, does that match your team?

**Tom Riordan:** Yeah, that's about right for my side. Patching cycles alone take a meaningful chunk of engineering time each quarter.

**Consultant:** Marcus, you mentioned the quarterly release cycle. What does the path look like to changing that — is it primarily the deployment infrastructure, or is it the application architecture?

**Marcus Webb:** Both, honestly. The commerce monolith is the biggest problem. It's a single deployable — any change anywhere requires a full regression cycle. We have teams that want to ship weekly and can't because they're blocked on the release train. The mobile APIs ship weekly because they're a separate service. That's what we want the whole organisation to look like.

**Tom Riordan:** The monolith is somewhere north of four million lines of Java. It's not going anywhere overnight.

**Consultant:** Right. So part of the architecture question is the decomposition strategy — how you break that apart alongside the infrastructure migration.

**Marcus Webb:** Exactly. We're not naïve about it — we know we're looking at a multi-year programme. The question is what we sequence first and what the right parallel workstreams are.

**Consultant:** Let's talk about the data side. You have customer data across 28 markets including EU. How are you thinking about data residency as part of this?

**David Yuen:** Non-negotiable that EU customer data stays in EU. That's regulatory, not a choice. APAC is a bit more complex — there are some residency requirements in specific jurisdictions we're still working through with legal. The payments data is separately scoped — PCI environment, physically isolated today, and whatever we do with it has to maintain that isolation.

**Priya Sharma:** The replication between our two data centres is also something that causes us problems. We get lag that shows up as inventory discrepancies. We've had cases where the same item was visible as in-stock in both regions simultaneously when there was only one left. At scale that's a real customer impact.

**Consultant:** Is that latency, consistency model, or something else?

**Tom Riordan:** Combination. The inter-DC link is fine under normal load. It degrades under peak. And some of the inventory logic was written assuming eventual consistency would be fine — which is mostly true except right at the moment of checkout. That's the gap.

**Consultant:** Priya, on the topic of timeline — Marcus mentioned three years. Is that the internal expectation or is there pressure from the board?

**Priya Sharma:** It's both. Three years is board-committed. Within that, Marcus and I have different views on what's achievable in year one. I think year one is foundation — exit the first hardware refresh, get the observability stack modernised, prove out the deployment pipeline on one or two services. Marcus wants to move faster than that.

**Marcus Webb:** I do. I think we can do more in year one if we make the right bets early.

**Consultant:** Where would you each say year one ends? What does the finish line look like?

**Priya Sharma:** For me, year one is: cloud-native deployment pipeline operational for at least two services, observability consolidated onto a modern platform, and a clear decomposition plan for the monolith agreed across the engineering leads. That's a full year of real work.

**Marcus Webb:** I'd add: cloud environment established for the ticketing workload specifically. That one has the most immediate business impact and the most political urgency after January.

**Consultant:** That's helpful. One more area I want to make sure we cover — competitive context. Are you in conversations with other vendors on the infrastructure side?

**Marcus Webb:** We're talking to people. I won't pretend otherwise. We've had conversations with the major cloud providers. What I'll say is that we don't have a signed commitment anywhere and we're specifically interested in what an independent platform perspective looks like before we make infrastructure decisions.

**David Yuen:** I'd rather not get into specifics of who we've talked to, but yes, we've done some preliminary work.

**Consultant:** Understood. Last question from me — if you imagine sitting in a board presentation 12 months from now, what's the one slide that would tell you this programme is on track?

**Marcus Webb:** An engineering team that's shipped a feature that would have taken six months before and took six weeks. That's the metric I care about.

**Priya Sharma:** For me it's an SLA we haven't missed in three months.

**Tom Riordan:** No cancellations on the next major on-sale.

**David Yuen:** A bill that's lower than the one we were going to write for the hardware refresh.

**Consultant:** That's a good set of success criteria to build against. Okay — I think we have a solid picture. Let me summarise what I've heard and I'll come back with a proposed approach for next steps…

---

*[Summary and next-steps discussion — 10 minutes — not transcribed]*

---

**Call ended:** 10:04 AM ET
