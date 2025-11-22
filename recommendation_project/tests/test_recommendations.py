import pytest
from recommendations.optimizer import SimpleKnowledgeBase, rank

def test_rank_ordering(sample_docs):
    kb = SimpleKnowledgeBase()
    for doc in sample_docs:
        kb.add_doc(doc)

    # add an extra fast bike doc with high popularity
    kb.add_doc({"id": "d4", "text": "fast bike", "popularity": 20})
    results = rank("fast", kb, top_k=2)
    assert isinstance(results, list)
    assert len(results) > 0
    # top doc should be one with 'fast' and high popularity
    assert results[0][0] in {"d4", "d2"}

def test_cache_effectiveness(sample_docs):
    kb = SimpleKnowledgeBase()
    for doc in sample_docs:
        kb.add_doc(doc)

    r1 = rank("apple", kb)
    kb.add_doc({"id": "d4", "text": "apple new", "popularity": 0})
    r2 = rank("apple", kb)
    assert r1 == r2
