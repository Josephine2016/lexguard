import os
from pathlib import Path

MODE = os.environ.get("LEXGUARD_LLM_MODE", "offline")  # "offline" (deterministic, no AWS needed) | "bedrock"
BEDROCK_MODEL = os.environ.get("LEXGUARD_BEDROCK_MODEL", "anthropic.claude-3-haiku-20240307")
BEDROCK_REGION = os.environ.get("AWS_REGION", "us-east-1")
CORPUS_PATH = Path(__file__).parent / "data" / "corpus" / "statutes.json"
CASES_PATH = os.environ.get("LEXGUARD_CASES_PATH", "cases.jsonl")
TABLE = os.environ.get("LEXGUARD_DYNAMODB_TABLE", "lexguard-cases")
