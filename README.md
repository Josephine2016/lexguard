# LexGuard — AI Legal-Access & Digital-Rights Agent
**LexHack 2026 · Open Innovation (AI & Law) · MVP**

LexGuard is a **functional AI agent** (not a dashboard) that gives ordinary Nigerians
instant, grounded legal guidance and then *does the follow-up work*: it drafts the
complaint, routes it to the right institution (NHRC, NDPC, Police Service Commission,
Legal Aid Council, DSVA…), escalates risky cases to human paralegals, and keeps the
case on file.

## The problem
Legal help in Nigeria is out of reach for most citizens: lawyers are unaffordable,
legal language is inaccessible, and people in crisis (unlawful detention, data leaks
by loan apps, online blackmail, domestic abuse) don't know their rights or where to
report. The result is silent, unrecorded rights violations.

## What the agent does (working MVP)
1. **Screens** every message for crisis indicators.
2. **Classifies** the issue into 8 legal categories (works with English + Pidgin input).
3. **Retrieves** the governing Nigerian statutes (TF-IDF now; Bedrock Knowledge Bases in prod).
4. **Composes** plain-language guidance with act/section citations.
5. **Acts**: routes to the correct institution and drafts a ready-to-review complaint letter.
6. **Escalates**: high-urgency / red-flag cases go to a human paralegal queue.
7. **Persists** every case (DynamoDB in prod).

## Run it
```bash
python -m lexguard.cli --demo                 # 3 canned citizen cases
python -m lexguard.cli "police collect money for bail..."   # your own case
LEXGUARD_LLM_MODE=bedrock LEXGUARD_ENV=aws AWS_REGION=eu-west-1 python -m lexguard.cli ...
```

## Architecture (AWS production)
```
WhatsApp/HTTP → API Gateway → Lambda (this agent graph)
      Bedrock (Claude 3 Haiku) ──grounding──▶ Bedrock Knowledge Bases
      DynamoDB (cases) · S3 (complaint docs) · SNS → WhatsApp follow-ups
```
Offline mode needs **zero dependencies** — deterministic composer, perfect for demos/tests.
Deploy with `sam deploy -t template.yaml --guided` (see docs/AWS_DEPLOYMENT.md).

## Repo map
| path | role |
|---|---|
| `lexguard/agent.py` | orchestration graph (screen→classify→retrieve→compose→act→escalate→persist) |
| `lexguard/categories.py` | 8-category legal taxonomy + classifier |
| `lexguard/retriever.py` | TF-IDF over statute corpus (swap → Knowledge Bases) |
| `lexguard/llm.py` | Offline composer ⇄ Amazon Bedrock Claude 3 Haiku |
| `lexguard/actions.py` | routing, complaint-letter drafts, persistence |
| `lexguard/guardrails.py` | crisis screen, disclaimers, human-in-the-loop |
| `lexguard/aws/` | Lambda handler + DynamoDB/S3/SNS wrappers |
| `docs/SUBMISSION.md` | the hackathon document (draft → critique → final) |
| `docs/DEVSWARM_WORKSPACES.md` | parallel-agent plan for DevSwarm Pro |
| `template.yaml` | SAM: API GW, Lambda, DynamoDB, S3, SNS, Bedrock IAM |
