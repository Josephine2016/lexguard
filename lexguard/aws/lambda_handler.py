"""Lambda entrypoint: WhatsApp/inbound HTTP -> LexGuardAgent -> case + response.
Body: {"from": "<phone>", "message": "<text>", "name": "<optional>"}
"""
import json
from ..agent import LexGuardAgent

_agent = None
def _get_agent():
    global _agent
    if _agent is None:
        _agent = LexGuardAgent()
    return _agent

def handle(event, context):
    body = json.loads(event.get("body") or "{}")
    msg = body.get("message", "").strip()
    if not msg:
        return {"statusCode": 400, "body": json.dumps({"error": "empty message"})}
    r = _get_agent().handle(msg, name=body.get("name", "Anonymous"), channel="whatsapp")
    reply = (r["answer"] + "\n\nRef: " + str(r["case_id"])
             + ("\n[HUMAN REVIEW QUEUED]" if r["human_review_required"] else ""))
    return {"statusCode": 200, "body": json.dumps({"reply": reply, "case_id": r["case_id"]})}
