# src/recommendations/recommendation_engine.py
"""
Recommendation Engine Module
----------------------------
This module searches the knowledge base using semantic similarity
and returns the top relevant answers for a given customer query.
"""

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch


class RecommendationEngine:
    """Searches the knowledge base and retrieves the most relevant results."""

    def __init__(self, knowledge_base_path: str):
        """
        Initialize the engine:
        - Load knowledge base (CSV)
        - Generate embeddings for each content entry
        """
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.kb = pd.read_csv(knowledge_base_path)

        # Compute embeddings for all KB entries
        self.kb['embedding'] = self.kb['content'].apply(
            lambda x: self.model.encode(x, convert_to_tensor=True)
        )

    def get_recommendations(self, query: str, top_k: int = 3) -> pd.DataFrame:
        """
        Returns top-k relevant knowledge base results for a cleaned query.
        """
        query_emb = self.model.encode(query, convert_to_tensor=True)

        # Compute similarity between query and KB entries
        similarities = [util.cos_sim(query_emb, emb).item() for emb in self.kb['embedding']]

        # Add similarity column and sort
        self.kb['similarity'] = similarities
        results = self.kb.sort_values(by='similarity', ascending=False).head(top_k)

        return results[['title', 'content', 'similarity']]


# ✅ Example (run this to test)
if __name__ == "__main__":
    from src.recommendations.query_processor import QueryProcessor

    qp = QueryProcessor()
    engine = RecommendationEngine("data/knowledge_base.csv")

    raw_query = "I forgot my password, how to reset?"
    clean_query = qp.clean_query(raw_query)
    results = engine.get_recommendations(clean_query)

    print(f"\nOriginal Query: {raw_query}")
    print(f"Cleaned Query : {clean_query}\n")
    print("Top Results:\n", results)
