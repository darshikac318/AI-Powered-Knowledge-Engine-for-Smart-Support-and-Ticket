from typing import Dict, List
from datetime import datetime

class StreamlitInterface:
    def __init__(self):
        self.session_history = []
    
    def log_query(self, query: str, results: List[Dict]):
        self.session_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'results_count': len(results)
        })
    
    def format_solution(self, solution: Dict) -> str:
        formatted = f"Source: {solution['source']}\n"
        formatted += f"Chunk: {solution['chunk_index'] + 1}/{solution['total_chunks']}\n\n"
        formatted += solution['content']
        return formatted
    
    def get_session_stats(self) -> Dict:
        return {
            'total_queries': len(self.session_history),
            'history': self.session_history
        }