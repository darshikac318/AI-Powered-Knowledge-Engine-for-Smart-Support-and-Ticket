import sys
import os
import warnings
warnings.filterwarnings('ignore')

sys.path.append('src')

from chroma_db import KnowledgeBaseDB

def display_results(query, results):
    print(f"\nQuery: '{query}'")
    print("-"*70)
    
    if not results['ids'] or not results['ids'][0]:
        print("No results found")
        return
    
    print(f"Found {len(results['ids'][0])} relevant results:\n")
    
    for i in range(len(results['ids'][0])):
        doc_id = results['ids'][0][i]
        content = results['documents'][0][i]
        metadata = results['metadatas'][0][i]
        
        print(f"{i+1}. Source: {metadata['source_file']}")
        print(f"   Chunk: {metadata['chunk_index'] + 1}/{metadata['total_chunks']}")
        print(f"   Content: {content[:250]}...")
        print()

def main():
    print("\n" + "="*70)
    print(" "*15 + "KNOWLEDGE BASE QUERY SYSTEM")
    print("="*70)
    
    try:
        kb = KnowledgeBaseDB()
        total = kb.count()
        sources = kb.get_all_sources()
        
        print(f"\nKnowledge Base Status:")
        print(f"  Total Chunks: {total}")
        print(f"  Source Documents: {len(sources)}")
        print(f"\nDocuments in Knowledge Base:")
        for i, source in enumerate(sources, 1):
            print(f"  {i}. {source}")
        
        print("\n" + "="*70)
        print("Running Test Queries")
        print("="*70)
        
        test_queries = [
            "How to return a product on Amazon",
            "What is the refund policy",
            "Replacement for damaged items",
            "Return window period for electronics"
        ]
        
        for query in test_queries:
            results = kb.search(query, n_results=3)
            display_results(query, results)
            print("-"*70)
        
        print("\n" + "="*70)
        print(" "*20 + "DEMO COMPLETE")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nError: {str(e)}\n")

if __name__ == "__main__":
    main()