"""Run:  python -m lexguard.cli \"your message\"   |   python -m lexguard.cli --demo   |   python -m lexguard.cli (interactive)
Env:   LEXGUARD_LLM_MODE=bedrock  LEXGUARD_ENV=aws  AWS_REGION=eu-west-1"""
import sys, json
from .agent import LexGuardAgent

DEMO_CASES = [
  ("Chika", "Police arrested my brother at a checkpoint in Ikeja yesterday and they are asking for 50,000 naira before they release him. They have not taken him to any station."),
  ("Ada", "My ex is threatening to post my nude pictures on Instagram if I do not get back together with him. I am scared."),
  ("Tunde", "A loan app downloaded my contact list and is now calling my boss and my family saying I owe them money. I never agreed to this."),
]

def show(r):
    print("=" * 78)
    print(f"CASE {r['case_id']}  |  category: {r['category_label']} (conf {r['confidence']})  |  engine: {r['llm']}")
    if r.get("crisis_hits"): print("CRISIS HITS:", r["crisis_hits"])
    print("-" * 78 + "\nGROUNDING:")
    for g in r["grounding"]:
        print(f"  [{g['score']:.4f}] {g['act']} {g['section']} — {g['title']}")
    print("-" * 78 + "\nANSWER:\n" + r["answer"])
    if r["institutions"]:
        print("-" * 78 + "\nROUTE -> " + " | ".join(r["institutions"]))
    if r["human_review_required"]:
        print("** QUEUED FOR HUMAN PARALEGAL REVIEW **")
    if r["draft_complaint"]:
        print("-" * 78 + "\nDRAFT COMPLAINT (first institution):\n" + r["draft_complaint"])

def main(argv):
    agent = LexGuardAgent()
    if argv and argv[0] == "--demo":
        for name, msg in DEMO_CASES:
            print(f"\n### Citizen ({name}): {msg}")
            show(agent.handle(msg, name=name))
        return
    if argv:
        show(agent.handle(" ".join(argv)))
        return
    print("LexGuard interactive (empty line to quit)")
    while True:
        try: msg = input("\ncitizen> ").strip()
        except (EOFError, KeyboardInterrupt): break
        if not msg: break
        show(agent.handle(msg))

if __name__ == "__main__":
    main(sys.argv[1:])
