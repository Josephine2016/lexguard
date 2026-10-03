# LexHack 2026 — Project Submission Document
**Project:** LexGuard — AI Legal-Access & Digital-Rights Agent for Nigeria
**Track:** Open Innovation (AI & Law) · **Stack:** Amazon Bedrock, Lambda, DynamoDB, S3, SNS, API Gateway
**Deadline: ~1 Oct 2026 (9 days from 22 Sep 2026 per organizer email) · Sponsor perk: 1 month DevSwarm Pro free (devswarm.ai + organizer code)**
**See `docs/EXECUTION_PLAN.md` for the day-by-day schedule.**

---

## 1. Problem Statement
Most Nigerians who face rights violations — unlawful detention, police extortion, loan-app
data leaks, online blackmail, domestic abuse — never get legal help. Lawyers are
unaffordable, statutes are written in inaccessible language, and citizens don't know
which institution (NHRC, NDPC, PSC, Legal Aid Council) handles their issue. The outcome:
silent, unrecorded violations and no paper trail for accountability.

## 2. Solution
LexGuard is a conversational **AI agent** (WhatsApp-first) that (a) understands a
citizen's problem in plain English or Pidgin, (b) answers with rights grounded in the
actual statute — cited by act and section, (c) **drafts the complaint** to the correct
institution, (d) escalates dangerous cases to human paralegals, and (e) keeps every case
on record. It is a working agent pipeline, not a dashboard.

## 3. Objectives — the double-checked version

### 3.1 Draft v1 (quick pass)
- [ ] Help people know their rights
- [ ] Make legal help faster and cheaper
- [ ] Use AI to improve access to justice
- [ ] Connect citizens with government agencies

### 3.2 Agent critique of v1 (what's wrong)
| # | Flaw | Why judges/markers penalize it |
|---|---|---|
| 1 | "Help people know their rights" — vague verb, no target, no number | Not measurable; cannot be tested or demoed against |
| 2 | "faster and cheaper" — compared to what? baseline missing | No baseline ⇒ no claimed improvement ⇒ no impact score |
| 3 | "Use AI to improve access to justice" — technology-first, not user-first | Describes a tool, not an outcome; judges score impact, not stack |
| 4 | "Connect citizens with agencies" — no named agency, no deliverable produced | No artefact = nothing to evaluate; ignores the real bottleneck (the citizen never files) |
| 5 | Missing: grounding/accuracy objective (critical for legal AI) | Un-grounded legal AI is a liability, not a solution |
| 6 | Missing: safety objective | GBV/detention cases mishandled = disqualifying risk |

### 3.3 Final objectives (v2 — approve these)
1. **Grounded answers or nothing:** every legal claim LexGuard makes cites act + section
   from a curated statute corpus; ungroundable questions are refused and routed to a
   human, never hallucinated. *Target: 100% citation coverage; demo test = 10/10 cases.*
2. **From question to filed complaint in one conversation:** within a single chat, produce
   a review-ready complaint draft addressed to the correct institution for ≥8 issue
   categories (detention, police misconduct, data rights, cyber-harassment, GBV, tenancy,
   consumer, labour). *Measured: draft generated in demo for each category.*
3. **Urgency-aware triage:** crisis keywords and red-flag indicators (detention >24h,
   threats, GBV) trigger immediate human-paralegal escalation. *Measured: 3/3 red-flag
   demo cases escalated (verified in demo run).*
4. **Accessible by design:** respond in the citizen's language/register (English, Pidgin,
   expandable to Yorùbá/Igbo/Hausa); plain-language reading level. *Measured: 2-language
   demo.*
5. **Institutional paper trail:** every case is persisted with category, grounding,
   routing and escalation status, producing the first citizen-side record of rights
   violations at scale (DynamoDB; analytics later). *Measured: case_id returned per case.*
6. **Free at the point of use, cost-efficient to run:** serverless AWS stack; offline
   deterministic mode costs ₦0 for demos/tests. *Measured: `sam deploy` bill ≈ $0 at demo
   volume.*

## 4. Use case → capability map (basis for objectives)
| Use case | Agent capability | Statutory grounding (verify before finals) |
|---|---|---|
| Brother held at checkpoint, bail demanded | unlawful_detention → Legal Aid/PSC/NHRC + ACJA s.8 steps | CFRN s.35; ACJA s.6/s.8; Police Act 2020 |
| Ex threatening to leak intimate images | cyber_harassment (+GBV) → Police cyber unit/NHRC, escalation | Cybercrimes Act s.24; VAPP Act |
| Loan app leaked contact list | digital_rights → NDPC complaint draft | NDPA 2023 (incl. s.40); CFRN s.37 |
| Illegal lockout by landlord | landlord_tenant → Mediation Center | Lagos Tenancy Law 2011 |
| Defective goods / undelivered service | consumer → FCCPC | FCCPA 2018 |

## 5. Technical architecture
`intake (API GW / WhatsApp webhook) → Lambda → agent graph`:
screen → classify → retrieve → compose (Bedrock Claude 3 Haiku, grounding injected) →
route → draft complaint → escalation queue → persist (DynamoDB; docs in S3; follow-ups SNS).
Swap points: retriever → Bedrock Knowledge Bases; classifier → Bedrock JSON-mode;
offline mode for zero-cost demos.

## 6. Ethics & safety
No legal advice — information + drafting only, with disclaimer on every reply; human
review mandatory for critical/high urgency and all red-flag cases; PII minimization;
crisis protocol (emergency services first). Legal information is grounded, dated, and
flagged for verification against the official gazette.

## 7. Impact & measurement
Cases handled, % with citations, % escalated correctly, time-to-draft, institutions
routed to. Long-term: a citizen-side violation dataset enabling accountability research.

## 8. Validated research query bank (use exactly these; add year operators)
| Purpose | Query | Where |
|---|---|---|
| Legal-aid gap stats | `access to justice Nigeria statistics legal aid gap` `site:worldbank.org Nigeria access to justice` | WB, UNDP |
| Statutes (primary law) | `Administration of Criminal Justice Act 2015 pdf` `Nigeria Data Protection Act 2023 pdf` | Laws of the Federation / gazette |
| Police accountability | `Police Act 2020 Nigeria pdf` `Police Complaints Response Unit` | official gazette / NPF |
| Digital-rights context | `loan apps Nigeria data privacy contact list investigation` `NDPC enforcement notice` | FCCPC/NDPC releases, press |
| GBV instruments | `VAPP Act 2015 Nigeria text` `Lagos DSVA` | state ministry sites |
| Benchmark prior art | `Stanford LLM x law hackathon winners access to justice` | CodeX, to position novelty |
| Judging alignment | `<your event site> rules judging criteria` | LexHack organizer page |
