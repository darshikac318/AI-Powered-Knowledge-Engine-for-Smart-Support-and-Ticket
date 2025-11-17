import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chroma_db import KnowledgeBaseDB
from recommendations.query_processor import QueryProcessor

class RecommendationEngine:
    def __init__(self):
        self.kb = KnowledgeBaseDB()
        self.processor = QueryProcessor()
<<<<<<< HEAD
    
    def get_recommendations(self, customer_query: str, top_k: int = 3):
        processed = self.processor.process_query(customer_query)
        
        results = self.kb.search(processed['cleaned'], n_results=top_k)
        
        recommendations = []
        
=======

    def get_recommendations(self, customer_query: str, top_k: int = 3):
        processed = self.processor.process_query(customer_query)

        results = self.kb.search(processed['cleaned'], n_results=top_k)

        recommendations = []

>>>>>>> cbc81c9cf4a0e207fdcc3fec1ef612c4bdff58d4
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                recommendations.append({
                    'article_id': results['ids'][0][i],
                    'source': results['metadatas'][0][i]['source_file'],
                    'content': results['documents'][0][i],
                    'relevance': 1.0 - (i * 0.1)
                })
<<<<<<< HEAD
        
=======

>>>>>>> cbc81c9cf4a0e207fdcc3fec1ef612c4bdff58d4
        return {
            'query_info': processed,
            'recommendations': recommendations,
            'total_found': len(recommendations)
        }