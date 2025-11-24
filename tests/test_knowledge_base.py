import unittest
import os
import sys
import tempfile
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestKnowledgeBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        cls.test_db_path = os.path.join(cls.test_dir, "test_chroma")
    
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
    
    def test_chromadb_initialization(self):
        try:
            import chromadb
            from chromadb.config import Settings
            
            client = chromadb.PersistentClient(
                path=self.test_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            self.assertIsNotNone(client)
            collection = client.create_collection("test_collection")
            self.assertIsNotNone(collection)
            client.delete_collection("test_collection")
            
        except ImportError:
            self.skipTest("ChromaDB not installed")
    
    def test_embedding_generation(self):
        try:
            from sentence_transformers import SentenceTransformer
            
            model = SentenceTransformer('all-MiniLM-L6-v2')
            text = "Test query for embedding"
            embedding = model.encode(text)
            
            self.assertIsNotNone(embedding)
            self.assertEqual(len(embedding), 384) 
            texts = ["Query 1", "Query 2", "Query 3"]
            embeddings = model.encode(texts)
            
            self.assertEqual(len(embeddings), 3)
            self.assertEqual(len(embeddings[0]), 384)
            
        except ImportError:
            self.skipTest("sentence-transformers not installed")
    
    def test_document_storage_and_retrieval(self):
        try:
            import chromadb
            from chromadb.config import Settings
            from sentence_transformers import SentenceTransformer
            
            client = chromadb.PersistentClient(
                path=self.test_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            collection = client.create_collection("test_docs")
            
            documents = [
                "How to return a product?",
                "What is the refund policy?",
                "How long does shipping take?"
            ]
            ids = ["doc1", "doc2", "doc3"]
            embeddings = model.encode(documents).tolist()
            
            collection.add(
                documents=documents,
                embeddings=embeddings,
                ids=ids
            )
            
            query = "return policy"
            query_embedding = model.encode(query).tolist()
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=2
            )
            
            self.assertIsNotNone(results)
            self.assertEqual(len(results['documents'][0]), 2)
            
            client.delete_collection("test_docs")
            
        except ImportError as e:
            self.skipTest(f"Required package not installed: {e}")
    
    def test_semantic_search_relevance(self):
        try:
            import chromadb
            from chromadb.config import Settings
            from sentence_transformers import SentenceTransformer
            
            client = chromadb.PersistentClient(
                path=self.test_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            collection = client.create_collection("semantic_test")
            documents = [
                "You can return products within 30 days of purchase",
                "We offer free shipping on orders over $50",
                "Customer service is available 24/7 via phone and email",
                "Refunds are processed within 5-7 business days"
            ]
            ids = [f"doc{i}" for i in range(len(documents))]
            embeddings = model.encode(documents).tolist()
            
            collection.add(
                documents=documents,
                embeddings=embeddings,
                ids=ids
            )
            
            query = "How do I get my money back?"
            query_embedding = model.encode(query).tolist()
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=2
            )
            
            top_result = results['documents'][0][0]
            self.assertTrue(
                'return' in top_result.lower() or 'refund' in top_result.lower(),
                f"Expected return/refund related result, got: {top_result}"
            )
            
            client.delete_collection("semantic_test")
        except ImportError as e:
            self.skipTest(f"Required package not installed: {e}")
    
    def test_multiple_query_handling(self):
        try:
            import chromadb
            from chromadb.config import Settings
            from sentence_transformers import SentenceTransformer
            import time
            
            client = chromadb.PersistentClient(
                path=self.test_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            collection = client.create_collection("multi_query_test")

            documents = [f"Document {i} about various topics" for i in range(10)]
            ids = [f"doc{i}" for i in range(10)]
            embeddings = model.encode(documents).tolist()
            
            collection.add(
                documents=documents,
                embeddings=embeddings,
                ids=ids
            )
            queries = ["topic 1", "topic 2", "topic 3"]
            
            start_time = time.time()
            for query in queries:
                query_embedding = model.encode(query).tolist()
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=3
                )
                self.assertIsNotNone(results)
            end_time = time.time()
            self.assertLess(end_time - start_time, 5.0)
            client.delete_collection("multi_query_test")
            
        except ImportError as e:
            self.skipTest(f"Required package not installed: {e}")
    
    def test_empty_query_handling(self):
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embedding = model.encode("")
            self.assertIsNotNone(embedding)
            self.assertEqual(len(embedding), 384)
            embedding = model.encode("   ")
            self.assertIsNotNone(embedding)
            
        except ImportError:
            self.skipTest("sentence-transformers not installed")

def run_tests():
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()