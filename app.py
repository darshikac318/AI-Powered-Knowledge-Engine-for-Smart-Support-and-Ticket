import streamlit as st
import sys
import os

sys.path.append('src')

from recommendations.recommendation_engine import RecommendationEngine

st.set_page_config(
    page_title="AI Support Agent Interface",
    page_icon="icon",
    layout="wide"
)

if 'engine' not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        st.session_state.engine = RecommendationEngine()

st.title("AI-Powered Support Agent Interface")
st.markdown("### Amazon Returns & Replacements Knowledge System")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Customer Query")
    
    customer_query = st.text_area(
        "Enter customer question:",
        height=150,
        placeholder="Example: How do I return a damaged product?",
        key="customer_query"
    )
    
    search_button = st.button("Search Knowledge Base", type="primary", use_container_width=True)

with col2:
    st.subheader("Knowledge Base Status")
    
    try:
        total_chunks = st.session_state.engine.kb.count()
        sources = st.session_state.engine.kb.get_all_sources()
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Total Chunks", total_chunks)
        with metric_col2:
            st.metric("Documents", len(sources))
        
        with st.expander("View All Documents"):
            for i, source in enumerate(sources, 1):
                st.text(f"{i}. {source}")
    except:
        st.error("Knowledge base not loaded")

st.markdown("---")

if search_button and customer_query:
    with st.spinner("Searching knowledge base..."):
        results = st.session_state.engine.get_recommendations(customer_query, top_k=5)
    
    st.subheader("Query Analysis")
    
    analysis_col1, analysis_col2 = st.columns(2)
    with analysis_col1:
        st.info(f"Detected Intent: {results['query_info']['intent'].upper()}")
    with analysis_col2:
        st.info(f"Results Found: {results['total_found']}")
    
    st.markdown("---")
    
    if results['recommendations']:
        st.subheader("Recommended Solutions for Agent")
        
        for idx, rec in enumerate(results['recommendations'], 1):
            with st.expander(f"Solution {idx} - {rec['source']}", expanded=(idx==1)):
                st.markdown(f"**Source Document:** {rec['source']}")
                st.markdown(f"**Relevance Score:** {rec['relevance']:.0%}")
                
                st.markdown("**Solution Content:**")
                st.info(rec['content'])
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"Use This Solution", key=f"use_{idx}"):
                        st.session_state[f'selected_solution_{idx}'] = rec['content']
                        st.success(f"Solution {idx} selected")
                
                with col_b:
                    if st.button(f"Copy Content", key=f"copy_{idx}"):
                        st.code(rec['content'], language=None)
        
        st.markdown("---")
        st.subheader("Agent Response to Customer")
        
        agent_response = st.text_area(
            "Compose response to customer:",
            value=results['recommendations'][0]['content'] if results['recommendations'] else "",
            height=200,
            key="agent_response"
        )
        
        if st.button("Send Response to Customer", type="primary"):
            st.success("Response sent to customer")
            st.balloons()
    
    else:
        st.warning("No relevant solutions found")

else:
    st.info("Enter a customer query above and click Search Knowledge Base to get started")

st.markdown("---")

with st.sidebar:
    st.header("How to Use")
    st.markdown("""
    Step 1: Agent receives customer question
    
    Step 2: Enter query in the text box
    
    Step 3: Click Search Knowledge Base
    
    Step 4: Review recommended solutions
    
    Step 5: Select best solution
    
    Step 6: Send response to customer
    """)
    
    st.markdown("---")
    
    st.header("System Info")
    st.markdown("""
    Embedding Model: all-MiniLM-L6-v2
    
    Chunking Method: Semantic AI
    
    Search Type: Vector Similarity
    
    Database: ChromaDB
    """)
    
    st.markdown("---")
    
    if st.button("Reload System"):
        st.cache_data.clear()
        st.rerun()