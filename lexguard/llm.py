"""LLM abstraction. Offline mode = deterministic template composer (runs anywhere,
zero cost, perfect for demos and tests). Bedrock mode = Amazon Bedrock
(Claude 3 Haiku) with the statute excerpts injected as grounding context.
"""
import json

class OfflineLLM:
    name = "offline-template-composer"
    def compose(self, message, category, hits):
        cat_label = hits and category or "a legal issue"
        grounds = "\n".join(
            f"  - {d['title']}: \"{excerpt(d['text'])}\"" for _, d in hits[:3])
        steps = {
            "unlawful_detention": [
                "Ask the officers for the reason for the arrest and which station the person is being taken to (ACJA s.8).",
                "Do not pay any money for release — bail is free; demand to see the Officer in Charge or a superior officer.",
                "If not released or charged within 24 hours, contact the Legal Aid Council and the NHRC immediately.",
                "Write down officer names, patrol car number, time and place now, while memory is fresh.",
            ],
            "police_misconduct": [
                "Do not resist physically; comply, then document (time, place, officer description, witnesses).",
                "Report to the Police Complaints Response Unit / Police Service Commission and the NHRC.",
                "You may be entitled to compensation for unlawful arrest or degrading treatment (Constitution s.35(6)).",
            ],
            "digital_rights": [
                "Revoke the app\u2019s permissions and document the leak (screenshots, dates).",
                "Send a written request to the company to stop processing and delete your data (NDPA data-subject rights).",
                "Lodge a complaint with the NDPC — it can investigate and issue enforcement notices and fines.",
            ],
            "cyber_harassment": [
                "Preserve all evidence — screenshots, call logs, URLs — before blocking or reporting.",
                "Report to the police cybercrime unit; cyberstalking and threats are criminal offences.",
                "If intimate images are involved, do not pay; paying escalates. Report immediately.",
            ],
            "gbv": [
                "Your safety comes first — if in immediate danger call emergency services and get to a safe place.",
                "The VAPP Act protects you: threats, coercion and abuse by a partner are offences, not \u201cfamily matters\u201d.",
                "Contact the DSVA (in Lagos) or NHRC; protection orders are available.",
            ],
            "landlord_tenant": [
                "Your landlord must follow due process: valid quit notice, then a court order. Self-help eviction is unlawful.",
                "Do not move out under threat; document everything and seek the Citizens\u2019 Mediation Center.",
            ],
            "consumer": [
                "Gather receipts and evidence of the defective goods or undelivered service.",
                "Complain first to the seller in writing; then escalate to the FCCPC.",
            ],
            "employment": [
                "Document owed salaries (payslips, contracts, bank alerts).",
                "Report unpaid wages to the Ministry of Labour labour inspectorate.",
            ],
        }
        steps_txt = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(steps.get(category, ["Document everything, then contact the National Human Rights Commission for guidance."])))
        return (f"**What the law says** (grounded in Nigerian statute):\n{grounds}\n\n"
                f"**What you can do now**:\n{steps_txt}\n\n{DISCLAIMER()}")

class BedrockLLM:
    name = "amazon-bedrock/claude-3-haiku"
    def __init__(self, model, region):
        import boto3  # imported lazily so offline mode needs no AWS deps
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model = model
    def compose(self, message, category, hits):
        context = "\n\n".join(f"[{d['act']} {d['section']}] {d['text']}" for _, d in hits)
        system = ("You are LexGuard, a Nigerian civic-legal assistant. Answer in plain English or Nigerian Pidgin "
                  "(match the user). Use ONLY the provided statutory excerpts as legal grounding, cite act and "
                  "section for every claim, give concrete next steps, never invent laws, and end with the "
                  "disclaimer that this is general information, not legal advice.")
        prompt = f"Citizen message:\n{message}\n\nClassified category: {category}\n\nStatutory grounding:\n{context}\n\nCompose the guidance."
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 800,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        })
        resp = self.client.invoke_model(modelId=self.model, body=body)
        return json.loads(resp["body"].read())["content"][0]["text"]

def excerpt(text, n=170):
    return (text[:n].rsplit(" ", 1)[0] + "\u2026") if len(text) > n else text

def DISCLAIMER():
    from .guardrails import DISCLAIMER as D
    return D

def get_llm(mode, model, region):
    return BedrockLLM(model, region) if mode == "bedrock" else OfflineLLM()
