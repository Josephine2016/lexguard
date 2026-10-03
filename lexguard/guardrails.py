"""Safety layer: crisis detection, disclaimers, human-in-the-loop triggers.
Deliberately conservative — false escalations are cheap, missed crises are not.
"""
DISCLAIMER = ("I am LexGuard, an AI legal-access assistant, not a lawyer. This is general legal "
              "information, not legal advice. For your specific case, please confirm with a lawyer "
              "or the Legal Aid Council (free for those who cannot afford one).")

CRISIS_WORDS = ["kill", "suicide", "dying", "gunshot", "bleeding", "emergency", "dye"]

def crisis_check(message):
    m = message.lower()
    hits = [w for w in CRISIS_WORDS if w in m]
    return bool(hits), hits

def redflag_check(message, category):
    from .categories import CATEGORIES
    flags = CATEGORIES.get(category, {}).get("redflags", [])
    m = message.lower()
    return [f for f in flags if f in m]

def needs_human_review(confidence, category, redflags):
    from .categories import CATEGORIES
    urgency = CATEGORIES.get(category, {}).get("urgency", "medium")
    return urgency in ("critical", "high") or bool(redflags) or confidence < 0.45
