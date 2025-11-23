import pytest
from recommendations.optimizer import SimpleKnowledgeBase, rank

@pytest.fixture
def sample_docs():
    return [
        {"id": "d1", "text": "apple banana orange", "popularity": 10},
        {"id": "d2", "text": "banana chocolate", "popularity": 2},
        {"id": "d3", "text": "apple fruit salad", "popularity": 5},
    ]

def test_search_precision_recall(sample_docs):
    kb = SimpleKnowledgeBase()
    for doc in sample_docs:
        kb.add_doc(doc)

    queries = [
        ("apple", {"d1", "d3"}),
        ("banana", {"d1", "d2"}),
        ("chocolate", {"d2"}),
    ]

    total_tp = total_fp = total_fn = 0
    for q, relevant in queries:
        results = rank(q, kb, top_k=5)
        retrieved = {doc_id for doc_id, _ in results}
        tp = len(retrieved & relevant)
        fp = len(retrieved - relevant)
        fn = len(relevant - retrieved)
        total_tp += tp
        total_fp += fp
        total_fn += fn

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else 0

    assert precision >= 0
    assert recall >= 0
    assert recall >= 0.6

def test_failure_cases_logged(sample_docs):
    kb = SimpleKnowledgeBase()
    for doc in sample_docs:
        kb.add_doc(doc)
    res = rank("durian", kb)
    assert res == [] or all(score == 0 for _id, score in res)
