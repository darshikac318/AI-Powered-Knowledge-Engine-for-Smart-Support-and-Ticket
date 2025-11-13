import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chroma_db import KnowledgeBaseDB
from typing import Dict, List

class AgentInterface:
    def __init__(self):
        self.kb = KnowledgeBaseDB()
    
    def search_solutions(self, query: str, num_results: int = 5) -> List[Dict]:
        results = self.kb.search(query, n_results=num_results)
        
        solutions = []
        
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                solutions.append({
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'source': results['metadatas'][0][i]['source_file'],
                    'chunk_index': results['metadatas'][0][i]['chunk_index'],
                    'total_chunks': results['metadatas'][0][i]['total_chunks']
                })
        
        return solutions
    
    def get_knowledge_base_stats(self) -> Dict:
        total = self.kb.count()
        sources = self.kb.get_all_sources()
        
        return {
            'total_chunks': total,
            'total_documents': len(sources),
            'documents': sources
        }