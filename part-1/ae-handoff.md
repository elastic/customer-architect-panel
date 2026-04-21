# GOES — AE Handoff Notes

**From:** Sarah Chen, Enterprise Account Executive
**To:** CA Team
**Re:** GOES Discovery Call — Background & Prep
**Date:** 2 April 2026

---

Hey team — really glad we finally got this on the calendar. I've been working this account for just over 14 months so let me give you the full picture before we go in.

---

## Account History

We first got in the door through their observability team in early 2025. Did a small Elastic Cloud POC for APM on their mobile platform — went well technically, but the project stalled when the infrastructure budget got frozen mid-year. Nobody's fault, just bad timing.

The relationship stayed warm. Marcus (CTO) reached out to me personally three months ago after the ticketing platform embarrassment in January. That's what's driving the urgency now. They have board pressure, a hardware refresh bill they don't want to pay, and a new mandate to modernise. The POC is a genuine entry point into what could be a significant platform deal.

---

## Stakeholders

**Marcus Webb, CTO** — Our champion. Joined 18 months ago from a hyperscaler background, which is why he's been the most vocal cloud advocate internally. He's smart, moves fast, and is visibly frustrated with the pace of the organisation. He wants to use this transformation to reshape the engineering culture. Be direct with him — he doesn't love deck-heavy presentations.

**David Yuen, Enterprise Architect** — The one to watch. David's been at GOES for 11 years and has seen vendors come and go. He had a painful experience with a major cloud vendor over licensing about three years back and still brings it up. He's not anti-cloud but he's deeply sceptical of managed services and will probe on exit strategies. Don't dismiss his concerns — if you acknowledge the lock-in tradeoffs honestly he tends to respect that. **Don't use the phrase "vendor lock-in" unprompted** — it triggers a 10-minute tangent.

**Priya Sharma, VP Engineering** — Pragmatist. Her job is shipping, not architecture. She'll ask about migration risk, team capacity, and realistic timelines more than anyone else in the room. Marcus is optimistic about the 3-year horizon; Priya is the one keeping the numbers honest. If Priya believes the plan is executable, the project moves forward.

**Tom Riordan, Head of E-Commerce Technology** — Domain expert, not a decision-maker. Tom knows the application stack better than anyone. If you need to go deep on the monolith, data architecture, or peak traffic patterns, Tom's your source. He defers to Marcus on strategy but speaks freely on technical specifics.

---

## What's Really Driving This

Public story: cloud transformation for agility and cost. Real story: three things.

1. The ticketing platform failure in January was genuinely embarrassing. Two major concert on-sales collapsed. There was press coverage. A few congressional staffers asked questions. Marcus told me off the record that the CEO wants this fixed before the next stadium tour season.

2. They have an $85M hardware refresh coming. The CFO has made it clear that writing that cheque again is off the table — they'd rather put the money into a cloud migration.

3. Competitor velocity. The e-commerce team ships quarterly; their biggest competitors ship weekly. This is becoming a talent retention problem too.

---

## Competitive Situation

AWS has a relationship with their infrastructure team — one of their SAs has been in the building a few times. We don't know if there's an active POC. Azure pitched them on a hybrid architecture about six months ago; I don't think it went anywhere but I'm not certain. We are the only vendor with an existing footprint (Elastic on mobile APM) and an internal champion, which is an advantage.

**Watch out:** Don't overclaim on competitive comparisons. Marcus knows the landscape and will call it out.

---

## What a Win Looks Like

Near-term: a scoped CA engagement — 2–3 workshops, target-state architecture, migration roadmap. First workload: expand the Elastic APM footprint to cover the full observability stack.

Longer-term: Elastic as the observability and search platform across their cloud-native estate. The search use case (product catalogue + ticketing recommendations) is an interesting angle we haven't fully explored yet.

---

## Watch-Outs

- **Timeline pressure is real but don't over-commit.** Marcus will push for aggressive timelines. Priya will moderate. Stay grounded.
- **The CEO's risk sensitivity.** The CEO sits on the board of a company that had a very public cloud migration failure two years ago. This comes up. GOES leadership will want to see phased, low-risk delivery — not a big bang.
- **Payments is a sensitive topic.** They process payments in-house for external merchants. It's considered a strategic moat. Don't suggest outsourcing it.
- **David will ask about Kubernetes.** Their app dev lead has been pushing K8s; David thinks it's oversold for their maturity level. Acknowledge both sides.

---

Looking forward to debriefing after. Ping me if anything comes up.

— Sarah
