from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SearchOptimizer:
    def __init__(self, 
                 relevance_threshold: float = 0.5,
                 diversity_weight: float = 0.3,
                 recency_weight: float = 0.2):
        self.relevance_threshold = relevance_threshold
        self.diversity_weight = diversity_weight
        self.recency_weight = recency_weight
    
    def filter_by_relevance(self, 
                           results: List[Dict[str, Any]], 
                           threshold: float = None) -> List[Dict[str, Any]]:
        threshold = threshold or self.relevance_threshold
        return [r for r in results if r.get('score', 0) >= threshold]
    
    def rerank_by_diversity(self, 
                           results: List[Dict[str, Any]], 
                           embeddings: List[np.ndarray] = None) -> List[Dict[str, Any]]:
        if not results or len(results) <= 1:
            return results
        if embeddings is None or len(embeddings) != len(results):
            return results
        selected = []
        remaining_indices = list(range(len(results)))
        selected.append(0)
        remaining_indices.remove(0)
        while remaining_indices:
            max_mmr = -float('inf')
            best_idx = None
            
            for idx in remaining_indices:
                relevance = results[idx].get('score', 0)
                if selected:
                    similarities = [
                        cosine_similarity(
                            embeddings[idx].reshape(1, -1),
                            embeddings[s].reshape(1, -1)
                        )[0][0]
                        for s in selected
                    ]
                    diversity = 1 - max(similarities)
                else:
                    diversity = 1.0
                mmr = (1 - self.diversity_weight) * relevance + self.diversity_weight * diversity
                
                if mmr > max_mmr:
                    max_mmr = mmr
                    best_idx = idx
            
            if best_idx is not None:
                selected.append(best_idx)
                remaining_indices.remove(best_idx)
            else:
                break
        
        return [results[i] for i in selected]
    
    def boost_recent_results(self, 
                            results: List[Dict[str, Any]], 
                            timestamp_field: str = 'timestamp') -> List[Dict[str, Any]]:
        if not results:
            return results
        timestamps = [r.get(timestamp_field, 0) for r in results]
        if not timestamps or max(timestamps) == 0:
            return results
        
        max_timestamp = max(timestamps)
        boosted_results = []
        for result in results:
            result_copy = result.copy()
            timestamp = result.get(timestamp_field, 0)
            
            if timestamp > 0:
                recency_factor = timestamp / max_timestamp
                original_score = result_copy.get('score', 0)
                boosted_score = (
                    (1 - self.recency_weight) * original_score + 
                    self.recency_weight * recency_factor
                )
                result_copy['score'] = boosted_score
                result_copy['original_score'] = original_score
            
            boosted_results.append(result_copy)
        return sorted(boosted_results, key=lambda x: x.get('score', 0), reverse=True)
    
    def deduplicate_results(self, 
                           results: List[Dict[str, Any]], 
                           key_field: str = 'id',
                           similarity_threshold: float = 0.95) -> List[Dict[str, Any]]:
        if not results:
            return results
        
        seen_keys = set()
        unique_results = []
        
        for result in results:
            key = result.get(key_field)
            if key and key in seen_keys:
                continue
            unique_results.append(result)
            if key:
                seen_keys.add(key)
        
        return unique_results
    
    def optimize_results(self, 
                        results: List[Dict[str, Any]], 
                        embeddings: List[np.ndarray] = None,
                        max_results: int = 10) -> List[Dict[str, Any]]:
        if not results:
            return results

        filtered = self.filter_by_relevance(results)
        deduped = self.deduplicate_results(filtered)
        boosted = self.boost_recent_results(deduped)
        if embeddings and len(embeddings) == len(boosted):
            optimized = self.rerank_by_diversity(boosted, embeddings)
        else:
            optimized = boosted
        return optimized[:max_results]
    
    def calculate_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        if not results:
            return {
                "count": 0,
                "avg_score": 0.0,
                "min_score": 0.0,
                "max_score": 0.0
            }
        
        scores = [r.get('score', 0) for r in results]
        
        return {
            "count": len(results),
            "avg_score": np.mean(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "std_score": np.std(scores)
        }