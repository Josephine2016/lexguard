"""Dependency-free TF-IDF retriever over the statute corpus.
In production this is swapped for Amazon Bedrock Knowledge Bases (OpenSearch Serverless)
over the full Laws of the Federation corpus; the interface stays identical.
"""
import json, math, re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9\u2019']+")

def tokenize(text):
    return TOKEN_RE.findall(text.lower())

class TfIdfIndex:
    def __init__(self, docs):
        self.docs = docs
        self.doc_tokens = [tokenize(d["title"] + " " + " ".join(d.get("keywords", [])) + " " + d["text"]) for d in docs]
        self.df = Counter()
        for toks in self.doc_tokens:
            for t in set(toks):
                self.df[t] += 1
        self.N = len(docs)
        self.doc_vecs = [self._vec(toks) for toks in self.doc_tokens]

    def _vec(self, toks):
        tf = Counter(toks)
        n = max(1, len(toks))
        return {t: (c / n) * (math.log((1 + self.N) / (1 + self.df[t])) + 1) for t, c in tf.items()}

    def search(self, query, k=3):
        qv = self._vec(tokenize(query))
        scored = []
        for d, dv in zip(self.docs, self.doc_vecs):
            dot = sum(w * dv.get(t, 0.0) for t, w in qv.items())
            if dot > 0:
                scored.append((dot, d))
        scored.sort(key=lambda x: -x[0])
        return scored[:k]

def load_index(path):
    with open(path) as f:
        return TfIdfIndex(json.load(f))
