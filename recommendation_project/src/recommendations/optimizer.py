import math
import threading
from collections import defaultdict
from typing import List, Tuple

from recommendations.cache_manager import cache_query

class SimpleKnowledgeBase:
    """In-memory TF-IDF knowledge base for testing/demo.
    Documents are dicts with 'id', 'text', 'popularity' fields.
    """

    def __init__(self, documents: List[dict] = None):
        self.docs = {}
        if documents:
            for d in documents:
                self.docs[d['id']] = d
        self.N = len(self.docs)
        self.lock = threading.RLock()
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in text.split() if t.strip()]

    def _build_index(self):
        self.df = defaultdict(int)
        self.tf = {}
        for doc_id, doc in self.docs.items():
            tokens = self._tokenize(doc.get("text", ""))
            freqs = defaultdict(int)
            for t in tokens:
                freqs[t] += 1
            self.tf[doc_id] = freqs
            for t in freqs:
                self.df[t] += 1
        # precompute idf
        self.N = len(self.docs)
        self.idf = {t: math.log((self.N + 1) / (1 + c)) + 1 for t, c in self.df.items()}

    def add_doc(self, doc: dict):
        with self.lock:
            self.docs[doc["id"]] = doc
            self.N = len(self.docs)
            self._build_index()


def bm25_score(query_tokens: List[str], doc_id: str, kb: SimpleKnowledgeBase, k1=1.5, b=0.75):
    tf = kb.tf.get(doc_id, {})
    score = 0.0
    doc_len = sum(tf.values()) if tf else 0
    avgdl = sum(sum(tf.values()) for tf in kb.tf.values()) / (kb.N or 1)
    for q in query_tokens:
        if q not in kb.idf:
            continue
        idf = kb.idf[q]
        f = tf.get(q, 0)
        denom = f + k1 * (1 - b + b * doc_len / (avgdl or 1))
        score += idf * ((f * (k1 + 1)) / (denom or 1))
    return score


def rank(query: str, kb: SimpleKnowledgeBase, top_k: int = 10) -> List[Tuple[str, float]]:
    """Rank documents for a query. Uses caching to save repeated work."""

    def compute():
        tokens = [t.lower() for t in query.split() if t.strip()]
        scores = []
        for doc_id in kb.docs:
            s = bm25_score(tokens, doc_id, kb)
            # popularity boost (simple)
            pop = float(kb.docs[doc_id].get("popularity", 0))
            s = s * (1 + math.log(1 + pop))
            scores.append((doc_id, s))
        # filter zero scores for clarity
        scores = [(d, sc) for d, sc in scores if sc > 0]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    return cache_query(query, compute)
