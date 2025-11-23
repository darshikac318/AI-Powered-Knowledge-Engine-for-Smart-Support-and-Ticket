import pytest
from recommendations.optimizer import SimpleKnowledgeBase, rank

def test_query_tokenization(sample_docs):
    kb = SimpleKnowledgeBase()
    for doc in sample_docs:
        kb.add_doc(doc)

    res = rank("Apple BANANA", kb)
    assert isinstance(res, list)
    assert all(isinstance(x[0], str) and isinstance(x[1], float) for x in res)
    assert len(res) >= 0
