import os
import shutil
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from data_ingestion.pdf_processor import PDFProcessor

class EmbeddingGenerator:
    def __init__(self):
        print("\nInitializing system...")
        
        print("Loading embedding model: all-MiniLM-L6-v2")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.persist_directory = os.path.join("data", "processed")
        
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            print("Cleaned existing database")
        
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            metadata={"description": "Semantic AI-based knowledge base"}
        )
        
        print(f"ChromaDB initialized: {self.persist_directory}\n")
    
    def generate_embeddings(self, documents: list):
        if not documents:
            raise Exception("No documents to process")
        
        print(f"Generating embeddings for {len(documents)} semantic chunks...")
        
        ids = [doc['id'] for doc in documents]
        contents = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        print("Computing embeddings with transformer model...")
        embeddings = self.model.encode(
            contents, 
            show_progress_bar=True,
            batch_size=32,
            normalize_embeddings=True
        )
        
        print("Storing in ChromaDB...")
        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=contents,
            metadatas=metadatas
        )
        
        print(f"Successfully stored {len(documents)} chunks")
    
    def build_knowledge_base(self):
        print("="*70)
        print(" "*15 + "SEMANTIC AI KNOWLEDGE BASE BUILDER")
        print("="*70)
        
        processor = PDFProcessor()
        documents = processor.process_all_pdfs()
        
        self.generate_embeddings(documents)
        
        total_count = self.collection.count()
        
        print("\n" + "="*70)
        print(" "*15 + "KNOWLEDGE BASE COMPLETE")
        print("="*70)
        print(f"Total chunks: {total_count}")
        print(f"Location: {self.persist_directory}")
        print(f"Method: Automatic semantic chunking with AI")
        print("="*70)

if __name__ == "__main__":
    generator = EmbeddingGenerator()
    generator.build_knowledge_base()