import sys
import os
import warnings
warnings.filterwarnings('ignore')

sys.path.append('src')

from embedding_generator import EmbeddingGenerator

def main():
    print("\n" + "="*70)
    print(" "*15 + "AI-POWERED KNOWLEDGE BASE BUILDER")
    print("="*70)
    
    try:
        generator = EmbeddingGenerator()
        generator.build_knowledge_base()
        
        print("\n" + "="*70)
        print(" "*20 + "BUILD COMPLETE")
        print("\n" + "="*70)
        
    except Exception as e:
        print("\n" + "="*70)
        print("ERROR:", str(e))
        print("="*70 + "\n")
        raise

if __name__ == "__main__":
    main()