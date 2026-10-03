# LexGuard — 9-Day Execution Plan to Submission
**Deadline: ~1 October 2026 (organizer email, 22 Sept: "9 days until the LexHack 2026 submission deadline")**

| Day (2026) | Focus | Deliverable | Owner |
|---|---|---|---|
| Tue Sep 23 | Setup | Claim free DevSwarm Pro (devswarm.ai → sign up → add repo → enter organizer code); push LexGuard to GitHub; `python -m lexguard.cli --demo` runs clean on your machine | You |
| Wed Sep 24 | Verification | Verify every statute citation in `data/corpus/statutes.json` against official gazette / Laws of the Federation; fix any section numbers | Agent (W1) |
| Thu Sep 25 | Actions | Workspace 2: complaint PDF/docx artefacts to S3/outbox; SNS 48h follow-up scheduler | Agent (W2) |
| Fri Sep 26 | AWS deploy | Workspace 3: `sam build && sam deploy --guided`; enable Claude 3 Haiku in Bedrock model access; `curl` the `/intake` endpoint | You + Agent (W3) |
| Sat Sep 27 | E2E + channels | WhatsApp webhook (or End User Messaging) wired to `/intake`; full cloud test with a real case; LEXGUARD_LLM_MODE=bedrock verified | You |
| Sun Sep 28 | Pitch | Workspace 4: 7-slide deck + 90-sec demo script from DEMO_TRANSCRIPT.md | Agent (W4) |
| Mon Sep 29 | Docs | Final SUBMISSION.md: objectives v2, impact metrics, ethics, architecture diagram; proof-read against judging criteria | You + me |
| Tue Sep 30 | Buffer | Rehearse demo 3x; fix anything that breaks; freeze code | You |
| Wed Oct 1 | **SUBMIT** | Upload repo + deck + video before the deadline; keep a local copy of everything submitted | You |

## Hard rules
1. **Demo must run offline AND on AWS** — offline mode is your safety net if cloud fails on demo day.
2. No new features after Sep 28 — polish only.
3. Every legal claim in the deck carries an act/section citation (already verified on Sep 24).
4. Rehearse the 90-sec script until it fits 90 seconds.
