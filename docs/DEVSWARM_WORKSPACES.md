# DevSwarm Pro plan — parallel agent workspaces (FREE 1 month via LexHack sponsor)
DevSwarm runs each Builder as an isolated git worktree: one task, one branch, one agent.
Paste each prompt into a fresh workspace. I can't run DevSwarm for you (it's a local
Mac/Windows app needing your agent logins), so this file IS the coordination layer.

## Claim your free month (per organizer email, 22 Sep 2026)
1. Download DevSwarm at **devswarm.ai**
2. Sign up and add a repository (push LexGuard to GitHub first, then add it)
3. Enter the organizer promo code from the email (the code line is blurry in the photo — verify it, it looks like `LEXHACK2026`)
4. You get 1 month of DevSwarm Pro free ($8 value) → parallel coding agents across workspaces

**Setup order:** GitHub repo → DevSwarm → then spawn the 4 workspaces below in parallel.

## Workspace 1 — `feature/grounding-kb`  (Claude Code or Amazon Q — best at AWS)
> Replace lexguard/retriever.py with an Amazon Bedrock Knowledge Bases client
> (retrieve_and_generate against a `lexguard-laws` KB synced from S3). Keep the
> TfIdfIndex interface identical. Acceptance: `handle()` returns grounding with
> `source_uri` fields; offline mode still passes all tests.

## Workspace 2 — `feature/actions-integrations`  (any agent)
> Extend lexguard/actions.py: (1) NDPC/NHRC complaint templates as filled PDF/docx
> artifacts stored via lexguard/aws/clients.store_document; (2) SNS follow-up
> scheduler stub (EventBridge rule) that re-pings open human_review cases after 48h.
> Acceptance: `python -m lexguard.cli --demo` writes artefacts to outbox/.

## Workspace 3 — `feature/aws-iac-tests`  (Amazon Q or Codex — strong at IaC)
> Harden template.yaml: add CloudWatch alarms, least-privilege IAM scoping, WAF on
> API Gateway, and `tests/` with moto-based unit tests for DynamoDB/SNS wrappers.
> Acceptance: `sam validate` clean; `pytest tests/` green.

## Workspace 4 — `docs/submission-pitch`  (any agent — non-code)
> Turn docs/SUBMISSION.md into a 3-minute pitch deck (7 slides) + 90-second demo
> script using the --demo transcript. Acceptance: one claim per slide, every legal
> claim carries an act/section citation.

## Merge order
1 → 2 → 3 → 4; review each diff in DevSwarm Review Mode before merging to main.
