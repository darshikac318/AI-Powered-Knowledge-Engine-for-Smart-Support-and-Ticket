from src.recommendations.optimizer import SimpleKnowledgeBase, rank


docs = [
    {"id": "d1", "text": "apple banana orange", "popularity": 10},
    {"id": "d2", "text": "banana chocolate", "popularity": 2},
    {"id": "d3", "text": "apple fruit salad", "popularity": 5},
]

kb = SimpleKnowledgeBase()
for d in docs:
    kb.add_doc(d)

print(rank("apple", kb))
