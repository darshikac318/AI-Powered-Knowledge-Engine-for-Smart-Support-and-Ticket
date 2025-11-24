import unittest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.recommendations.cache_manager import CacheManager
from src.recommendations.optimizer import SearchOptimizer

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        self.cache = CacheManager(cache_dir="test_cache", ttl=10)
    
    def tearDown(self):
        self.cache.clear()
        if os.path.exists("test_cache"):
            import shutil
            shutil.rmtree("test_cache")
    
    def test_cache_set_and_get(self):
        self.cache.set("test query", {"results": [1, 2, 3]})
        result = self.cache.get("test query")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["results"], [1, 2, 3])
    
    def test_cache_miss(self):
        result = self.cache.get("nonexistent query")
        self.assertIsNone(result)
    
    def test_cache_with_kwargs(self):
        self.cache.set("query", {"data": "value"}, param1="a", param2="b")
        result1 = self.cache.get("query", param1="a", param2="b")
        self.assertIsNotNone(result1)
        result2 = self.cache.get("query", param1="different")
        self.assertIsNone(result2)
    
    def test_cache_expiry(self):
        import time
        
        cache = CacheManager(cache_dir="test_cache", ttl=1)
        cache.set("query", "value")
        self.assertIsNotNone(cache.get("query"))
        time.sleep(2)
        self.assertIsNone(cache.get("query"))
    
    def test_cache_clear(self):
        self.cache.set("query1", "value1")
        self.cache.set("query2", "value2")
        
        self.assertIsNotNone(self.cache.get("query1"))
        self.assertIsNotNone(self.cache.get("query2"))
        
        self.cache.clear()
        
        self.assertIsNone(self.cache.get("query1"))
        self.assertIsNone(self.cache.get("query2"))
    
    def test_cache_stats(self):
        self.cache.set("query1", "value1")
        self.cache.set("query2", "value2")
        
        stats = self.cache.get_stats()
        
        self.assertEqual(stats["memory_entries"], 2)
        self.assertGreaterEqual(stats["disk_entries"], 0)


class TestSearchOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = SearchOptimizer(
            relevance_threshold=0.5,
            diversity_weight=0.3,
            recency_weight=0.2
        )
    
    def test_filter_by_relevance(self):
        results = [
            {"id": 1, "score": 0.8},
            {"id": 2, "score": 0.6},
            {"id": 3, "score": 0.3},
            {"id": 4, "score": 0.9}
        ]
        
        filtered = self.optimizer.filter_by_relevance(results)
        
        self.assertEqual(len(filtered), 3)
        self.assertTrue(all(r["score"] >= 0.5 for r in filtered))
    
    def test_filter_with_custom_threshold(self):
        results = [
            {"id": 1, "score": 0.8},
            {"id": 2, "score": 0.6},
            {"id": 3, "score": 0.3}
        ]
        
        filtered = self.optimizer.filter_by_relevance(results, threshold=0.7)
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], 1)
    
    def test_deduplicate_results(self):
        results = [
            {"id": 1, "text": "Result 1"},
            {"id": 2, "text": "Result 2"},
            {"id": 1, "text": "Duplicate"},
            {"id": 3, "text": "Result 3"}
        ]
        
        deduped = self.optimizer.deduplicate_results(results, key_field="id")
        
        self.assertEqual(len(deduped), 3)
        ids = [r["id"] for r in deduped]
        self.assertEqual(ids, [1, 2, 3])
    
    def test_boost_recent_results(self):
        results = [
            {"id": 1, "score": 0.8, "timestamp": 100},
            {"id": 2, "score": 0.7, "timestamp": 200},
            {"id": 3, "score": 0.9, "timestamp": 150}
        ]
        
        boosted = self.optimizer.boost_recent_results(results)
        self.assertNotEqual(boosted[0]["score"], 0.8)
        timestamps = [r["timestamp"] for r in boosted]
        scores = [r["score"] for r in boosted]
        
        self.assertTrue(boosted[0]["timestamp"] >= boosted[-1]["timestamp"])
    
    def test_rerank_by_diversity(self):
        results = [
            {"id": 1, "score": 0.9},
            {"id": 2, "score": 0.8},
            {"id": 3, "score": 0.7}
        ]
        embeddings = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.9, 0.1, 0.0]),
            np.array([0.0, 0.0, 1.0])
        ]
        
        reranked = self.optimizer.rerank_by_diversity(results, embeddings)
        
        self.assertEqual(len(reranked), 3)
        self.assertEqual(reranked[0]["id"], 1)
    
    def test_optimize_results_full_pipeline(self):
        results = [
            {"id": 1, "score": 0.9, "timestamp": 100},
            {"id": 2, "score": 0.8, "timestamp": 200},
            {"id": 3, "score": 0.3, "timestamp": 150}, 
            {"id": 2, "score": 0.8, "timestamp": 200},
            {"id": 4, "score": 0.7, "timestamp": 180}
        ]
        
        optimized = self.optimizer.optimize_results(results, max_results=5)
        
        self.assertLessEqual(len(optimized), 5)
        self.assertTrue(all(r["score"] >= 0.5 for r in optimized))
        
        ids = [r["id"] for r in optimized]
        self.assertEqual(len(ids), len(set(ids)))
    
    def test_calculate_metrics(self):
        """Test metrics calculation"""
        results = [
            {"score": 0.9},
            {"score": 0.7},
            {"score": 0.8}
        ]
        
        metrics = self.optimizer.calculate_metrics(results)
        
        self.assertEqual(metrics["count"], 3)
        self.assertAlmostEqual(metrics["avg_score"], 0.8, places=1)
        self.assertEqual(metrics["min_score"], 0.7)
        self.assertEqual(metrics["max_score"], 0.9)
    
    def test_empty_results(self):
        results = []
        
        filtered = self.optimizer.filter_by_relevance(results)
        self.assertEqual(filtered, [])
        
        metrics = self.optimizer.calculate_metrics(results)
        self.assertEqual(metrics["count"], 0)
        
        optimized = self.optimizer.optimize_results(results)
        self.assertEqual(optimized, [])

def run_tests():
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()