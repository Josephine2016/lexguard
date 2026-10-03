"""Issue taxonomy + keyword classifier. In production the classifier is a
Bedrock prompt with JSON-schema output; the interface is identical.
"""
CATEGORIES = {
  "unlawful_detention": {
    "label": "Unlawful detention / arrest",
    "desc": "person arrested or held by police or others without lawful basis, bail demand, held beyond 24h, arrested in place of another",
    "keywords": ["arrest", "detain", "hold", "locked", "cell", "bail", "warrant", "checkpoint", "suspect", "police", "station", "iron", "cuff"],
    "institutions": ["Legal Aid Council of Nigeria", "National Human Rights Commission", "Police Service Commission (Complaints)"],
    "urgency": "high",
    "redflags": ["shot", "killed", "dying", "hospital", "torture"],
  },
  "police_misconduct": {
    "label": "Police misconduct / brutality",
    "desc": "extortion at checkpoint, extortion of money, brutality, torture, unlawful search of phone or person, intimidation by security agents",
    "keywords": ["extort", "bribe", "collect money", "threaten", "beat", "torture", "search my phone", "checkpoint", "harass", "slap", "gun"],
    "institutions": ["Police Service Commission (Complaints)", "National Human Rights Commission", "Legal Aid Council of Nigeria"],
    "urgency": "high",
    "redflags": ["shot", "killed", "gunshot", "bleeding"],
  },
  "digital_rights": {
    "label": "Digital rights / data protection",
    "keywords": ["data", "loan app", "contact list", "privacy", "leak", "consent", "personal information", "my pictures", "account", "hack", "otp"],
    "desc": "misuse or leak of personal data by apps or companies, privacy violations, unauthorized data sharing, account compromise",
    "institutions": ["Nigeria Data Protection Commission (NDPC)", "National Human Rights Commission"],
    "urgency": "medium",
    "redflags": ["blackmail", "nude"],
  },
  "cyber_harassment": {
    "label": "Online harassment / cyberstalking",
    "keywords": ["threat", "stalk", "harass online", "impersonat", "fake account", "cyberbully", "post my", "expose"],
    "desc": "threats, stalking, impersonation, image-based abuse or blackmail carried out online or by phone",
    "institutions": ["Nigeria Police (Cybercrime Unit)", "National Human Rights Commission"],
    "urgency": "high",
    "redflags": ["kill", "suicide", "nude", "blackmail", "rape"],
  },
  "gbv": {
    "label": "Gender-based violence / domestic abuse",
    "keywords": ["husband", "wife", "boyfriend", "girlfriend", "partner", "beat me", "domestic", "rape", "sexual", "abuse", "marry"],
    "desc": "violence, sexual abuse, coercion or threats by an intimate partner or family member",
    "institutions": ["National Human Rights Commission", "Lagos State Domestic & Sexual Violence Agency (DSVA)", "Nigeria Police (Gender Desk)"],
    "urgency": "critical",
    "redflags": ["kill", "weapon", "children watching", "locked inside", "pregnant"],
  },
  "landlord_tenant": {
    "label": "Landlord / tenancy dispute",
    "keywords": ["landlord", "tenant", "rent", "evict", "quit notice", "house", "apartment", "pack out", "lock"],
    "desc": "illegal eviction, rent disputes, harassment by landlord or agent",
    "institutions": ["Lagos State Citizens\u2019 Mediation Center", "Lagos State Ministry of Justice (Office of Public Defender)"],
    "urgency": "medium",
    "redflags": ["thugs", "violence", "armed"],
  },
  "consumer": {
    "label": "Consumer protection",
    "keywords": ["refund", "defective", "goods", "fake product", "paid for", "not deliver", "scam vendor", "warranty"],
    "desc": "defective goods, failure to deliver paid services, false advertising, unfair contract terms",
    "institutions": ["Federal Competition & Consumer Protection Commission (FCCPC)"],
    "urgency": "low",
    "redflags": [],
  },
  "employment": {
    "label": "Employment / labour rights",
    "keywords": ["salary", "wages", "owe me", "sack", "fired", "employer", "work", "gratuity", "pension"],
    "desc": "unpaid salaries, unfair termination, workplace rights",
    "institutions": ["Ministry of Labour & Employment (Labour Inspectorate)"],
    "urgency": "medium",
    "redflags": ["assault", "injured"],
  },
}

def classify(message):
    """Keyword-overlap classifier with Pidgin/English coverage. Returns (category_key, confidence 0-1)."""
    msg = message.lower()
    best, best_score = None, 0.0
    for key, cat in CATEGORIES.items():
        score = sum(1 for kw in cat["keywords"] if kw in msg)
        if score > best_score:
            best, best_score = key, score
    if best is None:
        return "general", 0.1
    # light saturation: 1 hit = low conf, 3+ hits = high conf
    conf = min(0.95, 0.35 + 0.2 * best_score)
    return best, conf
