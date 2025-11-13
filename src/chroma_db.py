import chromadb
from chromadb.config import Settings
import os

class KnowledgeBaseDB:
    def __init__(self, persist_directory=None):
        if persist_directory is None:
            persist_directory = os.path.join("data", "processed")
        
        if not os.path.exists(persist_directory):
            raise Exception(
                f"Knowledge base not found at {persist_directory}. "
                f"Run load_knowledge_base.py first to build the knowledge base."
            )
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base"
        )
    
    def search(self, query: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    
    def count(self):
        return self.collection.count()
    
    def get_all_sources(self):
        all_items = self.collection.get()
        sources = set()
        if all_items and 'metadatas' in all_items:
            for metadata in all_items['metadatas']:
                if 'source_file' in metadata:
                    sources.add(metadata['source_file'])
        return sorted(list(sources))