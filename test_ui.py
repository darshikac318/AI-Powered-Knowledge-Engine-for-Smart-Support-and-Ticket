import sys
sys.path.append('src')

from integrations.agent_interface import AgentInterface

def test_interface():
    print("Testing Agent Interface")
    print("="*70)
    
    agent = AgentInterface()
    
    stats = agent.get_knowledge_base_stats()
    print(f"\nKnowledge Base Stats:")
    print(f"  Total Chunks: {stats['total_chunks']}")
    print(f"  Documents: {stats['total_documents']}")
    
    print("\nTesting Search:")
    test_query = "How to return a product"
    
    solutions = agent.search_solutions(test_query, num_results=3)
    
    print(f"\nQuery: {test_query}")
    print(f"Results: {len(solutions)}")
    
    for i, solution in enumerate(solutions, 1):
        print(f"\nSolution {i}:")
        print(f"  Source: {solution['source']}")
        print(f"  Content: {solution['content'][:100]}...")
    
    print("\n" + "="*70)
    print("Test Complete")

if __name__ == "__main__":
    test_interface()