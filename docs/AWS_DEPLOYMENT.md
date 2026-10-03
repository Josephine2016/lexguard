# Deploying LexGuard to AWS (SAM)
1. `pip install aws-sam-cli boto3 && aws configure` (or an IAM role).
2. `sam build -t template.yaml && sam deploy --guided` (stack name `lexguard`, region e.g. `eu-west-1` — confirm Bedrock model access in that region).
3. Enable **Anthropic Claude 3 Haiku** in Bedrock → Model access (console).
4. (Optional, prod) Create a **Bedrock Knowledge Base** over the Laws of the Federation corpus in S3, swap `lexguard/retriever.py` for the KB client, and switch the classifier to Bedrock JSON mode.
5. Wire the **WhatsApp Business Cloud API** webhook (or AWS End User Messaging) to the `/intake` URL from stack Outputs.
6. Smoke test: `curl -X POST <ApiUrl> -d '{"from":"+234...","message":"police arrested my brother..."}'`.
Fallbacks: `LEXGUARD_LLM_MODE=offline` (deterministic composer), `LEXGUARD_ENV=local` (JSONL/print) — demo anywhere with zero AWS cost.
