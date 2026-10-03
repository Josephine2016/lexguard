"""LexGuard agent orchestrator.

Pipeline:  screen -> classify -> retrieve statutes -> compose grounded answer
          -> route institutions -> draft complaint -> human-review queue -> persist.
Every step is one tool; each tool is independently replaceable by its AWS
counterpart (see lexguard/aws/). This is the graph that the Lambda handler runs.
"""
from . import config, guardrails
from .actions import route, draft_complaint, save_case
from .categories import classify, CATEGORIES
from .llm import get_llm
from .retriever import load_index

class LexGuardAgent:
    def __init__(self, mode=None):
        mode = mode or config.MODE
        self.llm = get_llm(mode, config.BEDROCK_MODEL, config.BEDROCK_REGION)
        self.index = load_index(config.CORPUS_PATH)

    def handle(self, message, name="Anonymous", channel="cli", lang=None):
        # 1. crisis screen
        crisis, crisis_hits = guardrails.crisis_check(message)
        if crisis:
            return self._result(message, "crisis", None, [],
                "CRISIS PROTOCOL: immediate danger detected. Please contact emergency services (112) and get to safety. "
                "Legal help can follow once you are safe.", human_review=True, crisis_hits=crisis_hits)

        # 2. classify
        category, confidence = classify(message)

        # 3. retrieve statutory grounding
        hits = self.index.search(message, k=3)

        # 4. compose grounded guidance
        answer = self.llm.compose(message, category, hits)

        # 5. safety rails
        redflags = guardrails.redflag_check(message, category)
        human_review = guardrails.needs_human_review(confidence, category, redflags)
        if redflags:
            answer += ("\n\n[ESCALATED: this case includes risk indicators ({}). A human paralegal has been "
                       "alerted and will contact you.]").format(", ".join(redflags))

        # 6. actions: route + draft complaint for top institution
        institutions = route(category)
        case = {"message": message, "name": name, "category": category, "grounds": hits,
                "channel": channel, "language": lang}
        complaint = draft_complaint(institutions[0], case)

        # 7. persist
        case_id = save_case({**case, "confidence": confidence, "human_review": human_review,
                             "institutions": institutions}, config.CASES_PATH)
        return self._result(message, category, hits, answer, institutions, complaint, human_review, case_id, confidence)

    def _result(self, message, category, hits, answer, institutions=None, complaint=None,
                human_review=False, case_id=None, confidence=None, crisis_hits=None):
        return {
            "case_id": case_id, "category": category,
            "category_label": CATEGORIES.get(category, {}).get("label", "General / unclassified"),
            "confidence": confidence, "llm": self.llm.name,
            "grounding": [{"act": d["act"], "section": d["section"], "title": d["title"], "score": round(s, 4)} for s, d in (hits or [])],
            "answer": answer,
            "institutions": institutions or [],
            "draft_complaint": complaint,
            "human_review_required": human_review,
            "crisis_hits": crisis_hits,
        }
