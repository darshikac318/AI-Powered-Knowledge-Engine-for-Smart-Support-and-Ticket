import streamlit as st
import sys
import os
from datetime import datetime
import random

sys.path.append('src')

from database import Database

st.set_page_config(
    page_title="Amazon Knowledge Support System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }
    
    .stButton>button {
        background-color: #FF9900;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 500;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background-color: #FF8800;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .user-message {
        background: #666362;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
        margin-right: 20%;
    }
    
    .agent-message {
        background: #353839;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
        margin-left: 20%;
    }
    
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

db = Database()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'active_ticket' not in st.session_state:
    st.session_state.active_ticket = None

def login_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.title("Amazon Support System")
    st.subheader("Login")
    
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login", type="primary", use_container_width=True):
            role = db.authenticate_user(username, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with col2:
        if st.button("Clear", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    st.caption("Demo Credentials:")
    st.caption("User: user1 / user123")
    st.caption("Agent: agent1 / agent123")
    st.caption("Manager: manager1 / manager123")
    
    st.markdown('</div>', unsafe_allow_html=True)

def user_interface():
    st.title("Amazon Knowledge Support System")
    st.subheader(f"Welcome, {st.session_state.username}")
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["Raise Query", "Support Chat", "My Tickets"])
    
    with tab1:
        st.markdown("### Submit Your Query")
        st.info("We respect your privacy. Only Order ID and issue description are required.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Your Name", value=st.session_state.username)
        
        with col2:
            order_id = st.text_input("Order ID (Optional)", placeholder="123-4567890-1234567")
        
        query_type = st.selectbox(
            "Query Type",
            ["Select", "Return Request", "Replacement Request", "Refund Status", 
             "Damaged Product", "Wrong Item Received", "Other"]
        )
        
        query_text = st.text_area(
            "Describe Your Issue",
            height=150,
            placeholder="Provide details about your return or replacement request"
        )
        
        if st.button("Submit Query", type="primary", use_container_width=True):
            if customer_name and query_text and query_type != "Select":
                ticket_id = f"TKT{random.randint(10000, 99999)}"
                ticket_data = {
                    'ticket_id': ticket_id,
                    'customer_name': customer_name,
                    'order_id': order_id,
                    'query_type': query_type,
                    'query_text': query_text,
                    'status': 'Open',
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                db.create_ticket(ticket_data)
                st.success(f"Query submitted! Ticket ID: {ticket_id}")
                st.balloons()
            else:
                st.error("Please fill required fields: Name, Query Type, and Issue Description")
    
    with tab2:
        st.markdown("### Support Chat")
        
        user_tickets = [t for t in db.get_tickets() if t['customer_name'] == st.session_state.username]
        
        if user_tickets:
            ticket_options = [f"{t['ticket_id']} - {t['query_type']}" for t in user_tickets]
            selected = st.selectbox("Select Your Ticket", ticket_options)
            
            if selected:
                ticket_id = selected.split(" - ")[0]
                st.session_state.active_ticket = ticket_id
                
                if st.button("Refresh Chat"):
                    st.rerun()
                
                messages = db.get_chat_messages(ticket_id)
                
                st.markdown("### Conversation")
                
                for msg in messages:
                    if msg['sender'] == 'User':
                        st.markdown(f'<div class="user-message"><b>You:</b> {msg["message"]}<br><small>{msg["timestamp"]}</small></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="agent-message"><b>Support Agent:</b> {msg["message"]}<br><small>{msg["timestamp"]}</small></div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                user_msg = st.text_input("Type your message", key="user_chat")
                
                if st.button("Send", type="primary"):
                    if user_msg:
                        db.add_chat_message(ticket_id, "User", user_msg)
                        st.rerun()
        else:
            st.info("No tickets found. Please raise a query first.")
    
    with tab3:
        st.markdown("### My Tickets")
        
        my_tickets = [t for t in db.get_tickets() if t['customer_name'] == st.session_state.username]
        
        if my_tickets:
            for ticket in my_tickets:
                status_badge = "Resolved" if ticket['status'] == 'Resolved' else "In Progress" if ticket['status'] == 'In Progress' else "Open"
                status_color = "🟢" if ticket['status'] == 'Resolved' else "🟡" if ticket['status'] == 'In Progress' else "🔴"
                
                with st.expander(f"{status_color} Ticket {ticket['ticket_id']} - {status_badge}"):
                    st.markdown(f"**Query Type:** {ticket['query_type']}")
                    st.markdown(f"**Status:** {status_badge}")
                    st.markdown(f"**Created:** {ticket['created_at']}")
                    st.markdown(f"**Your Issue:** {ticket['query_text']}")
                    
                    if ticket['status'] == 'Resolved' and ticket.get('resolution_notes'):
                        st.success(f"**Resolution:** {ticket['resolution_notes']}")
                    elif ticket['status'] == 'In Progress':
                        st.info("Your ticket is being handled by our support team")
                    else:
                        st.warning("Waiting for agent to handle this ticket")
        else:
            st.info("No tickets yet")

def agent_interface():
    st.title("Support Agent Dashboard")
    st.subheader(f"Agent: {st.session_state.username}")
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["Ticket Queue", "Knowledge Base Search", "Active Chats"])
    
    with tab1:
        st.markdown("### Ticket Management")
        
        open_tickets = db.get_tickets('Open')
        progress_tickets = db.get_tickets('In Progress')
        resolved_tickets = db.get_tickets('Resolved')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Open", len(open_tickets))
        with col2:
            st.metric("In Progress", len(progress_tickets))
        with col3:
            st.metric("Resolved", len(resolved_tickets))
        
        st.markdown("---")
        st.markdown("### Open Tickets")
        
        if open_tickets:
            for ticket in open_tickets:
                with st.expander(f"{ticket['ticket_id']} - {ticket['query_type']}"):
                    st.markdown(f"**Customer:** {ticket['customer_name']}")
                    if ticket['order_id']:
                        st.markdown(f"**Order ID:** {ticket['order_id']}")
                    st.markdown(f"**Created:** {ticket['created_at']}")
                    st.info(ticket['query_text'])
                    
                    if st.button(f"Handle Ticket", key=f"handle_{ticket['ticket_id']}"):
                        db.update_ticket_status(ticket['ticket_id'], 'In Progress')
                        db.assign_agent(ticket['ticket_id'], st.session_state.username)
                        st.rerun()
        else:
            st.info("No open tickets")
        
        st.markdown("---")
        st.markdown("### In Progress Tickets")
        
        if progress_tickets:
            for ticket in progress_tickets:
                with st.expander(f"{ticket['ticket_id']} - In Progress"):
                    st.markdown(f"**Customer:** {ticket['customer_name']}")
                    st.markdown(f"**Query:** {ticket['query_text']}")
                    st.markdown(f"**Assigned to:** {ticket['assigned_agent']}")
                    
                    st.markdown("---")
                    st.markdown("**Customer Resolution (Visible to Customer)**")
                    
                    resolution_notes = st.text_area(
                        "How was the issue resolved?",
                        placeholder="Explain to customer how their issue was resolved...",
                        key=f"resolution_{ticket['ticket_id']}"
                    )
                    
                    st.markdown("---")
                    st.markdown("**Knowledge Base Feedback (For Developers Only - NOT visible to customer)**")
                    
                    kb_helpfulness = st.select_slider(
                        "How helpful was the Knowledge Base?",
                        options=["Very Poor", "Poor", "Average", "Good", "Excellent"],
                        value="Average",
                        key=f"kb_help_{ticket['ticket_id']}"
                    )
                    
                    kb_feedback = st.text_area(
                        "Knowledge Base Improvement Suggestions",
                        placeholder="Was KB accurate? Fast? What's missing? How to improve search?",
                        key=f"kb_feedback_{ticket['ticket_id']}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Resolve Ticket", key=f"resolve_{ticket['ticket_id']}", type="primary"):
                            if resolution_notes:
                                db.add_resolution_notes(ticket['ticket_id'], resolution_notes)
                                
                                kb_feedback_data = {
                                    'ticket_id': ticket['ticket_id'],
                                    'query_type': ticket['query_type'],
                                    'kb_helpfulness': kb_helpfulness,
                                    'kb_feedback': kb_feedback if kb_feedback else "No additional comments",
                                    'agent_name': st.session_state.username,
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                db.add_kb_feedback(kb_feedback_data)
                                
                                db.update_ticket_status(ticket['ticket_id'], 'Resolved')
                                st.success("Ticket resolved! KB feedback sent to developers.")
                                st.rerun()
                            else:
                                st.warning("Please add resolution notes for the customer")
                    
                    with col2:
                        if st.button(f"Request More Info", key=f"more_info_{ticket['ticket_id']}"):
                            db.add_chat_message(ticket['ticket_id'], "Agent", "I need more information to resolve your issue. Please provide additional details.")
                            st.info("Message sent to customer")
        else:
            st.info("No ongoing tickets")
    
    with tab2:
        st.markdown("### Search Knowledge Base")
        
        query_input = st.text_area("Enter Customer Query", height=100, placeholder="Example: Customer wants to return damaged product")
        
        if st.button("Search Solutions", type="primary"):
            if query_input:
                try:
                    from recommendations.recommendation_engine import RecommendationEngine
                    
                    if 'engine' not in st.session_state:
                        st.session_state.engine = RecommendationEngine()
                    
                    results = st.session_state.engine.get_recommendations(query_input, top_k=5)
                    
                    st.markdown("### Search Results")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"Intent: {results['query_info']['intent'].upper()}")
                    with col2:
                        st.info(f"Found: {results['total_found']} solutions")
                    
                    if results['recommendations']:
                        for idx, rec in enumerate(results['recommendations'], 1):
                            st.markdown(f"#### Solution {idx}")
                            st.markdown(f"**Source:** {rec['source']}")
                            st.markdown(f"**Relevance:** {rec['relevance']:.0%}")
                            st.info(rec['content'])
                            
                            if st.button(f"Copy Solution {idx}", key=f"copy_{idx}"):
                                st.code(rec['content'], language=None)
                            
                            st.markdown("---")
                    else:
                        st.warning("No solutions found in knowledge base")
                except Exception as e:
                    st.error(f"Error searching knowledge base: {str(e)}")
                    st.info("Make sure knowledge base is built: python load_knowledge_base.py")
    
    with tab3:
        st.markdown("### Active Chat Sessions")
        
        progress_tickets = db.get_tickets('In Progress')
        my_tickets = [t for t in progress_tickets if t['assigned_agent'] == st.session_state.username]
        
        if my_tickets:
            ticket_options = [f"{t['ticket_id']} - {t['customer_name']}" for t in my_tickets]
            selected = st.selectbox("Select Chat", ticket_options)
            
            if selected:
                ticket_id = selected.split(" - ")[0]
                
                if st.button("Refresh Chat"):
                    st.rerun()
                
                messages = db.get_chat_messages(ticket_id)
                
                st.markdown("### Conversation")
                
                for msg in messages:
                    if msg['sender'] == 'User':
                        st.markdown(f'<div class="user-message"><b>Customer:</b> {msg["message"]}<br><small>{msg["timestamp"]}</small></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="agent-message"><b>You:</b> {msg["message"]}<br><small>{msg["timestamp"]}</small></div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                agent_msg = st.text_input("Type response to customer", key="agent_chat")
                
                if st.button("Send Reply", type="primary"):
                    if agent_msg:
                        db.add_chat_message(ticket_id, "Agent", agent_msg)
                        st.rerun()
        else:
            st.info("No active chats assigned to you")

def manager_interface():
    st.title("Content Manager Dashboard")
    st.subheader(f"Manager: {st.session_state.username}")
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Knowledge Base Stats", "Ticket Analytics", "All Tickets", "KB Developer Feedback"])
    
    with tab1:
        st.markdown("### Knowledge Base Statistics")
        
        try:
            from chroma_db import KnowledgeBaseDB
            kb = KnowledgeBaseDB()
            total = kb.count()
            sources = kb.get_all_sources()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Chunks", total)
            with col2:
                st.metric("Documents", len(sources))
            
            st.markdown("### Source Documents")
            for i, source in enumerate(sources, 1):
                st.text(f"{i}. {source}")
        except Exception as e:
            st.error(f"Knowledge base not loaded: {str(e)}")
            st.info("Run: python load_knowledge_base.py")
    
    with tab2:
        st.markdown("### Ticket Analytics")
        
        all_tickets = db.get_tickets()
        open_count = len([t for t in all_tickets if t['status'] == 'Open'])
        progress_count = len([t for t in all_tickets if t['status'] == 'In Progress'])
        resolved_count = len([t for t in all_tickets if t['status'] == 'Resolved'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tickets", len(all_tickets))
        with col2:
            st.metric("Open", open_count)
        with col3:
            st.metric("In Progress", progress_count)
        with col4:
            st.metric("Resolved", resolved_count)
        
        st.markdown("---")
        st.markdown("### Query Type Distribution")
        
        query_types = {}
        for ticket in all_tickets:
            qtype = ticket['query_type']
            query_types[qtype] = query_types.get(qtype, 0) + 1
        
        for qtype, count in sorted(query_types.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"**{qtype}:** {count} tickets")
    
    with tab3:
        st.markdown("### All Tickets Overview")
        
        all_tickets = db.get_tickets()
        
        if all_tickets:
            for ticket in all_tickets:
                status_color = "🟢" if ticket['status'] == 'Resolved' else "🟡" if ticket['status'] == 'In Progress' else "🔴"
                
                with st.expander(f"{status_color} {ticket['ticket_id']} - {ticket['status']}"):
                    st.markdown(f"**Customer:** {ticket['customer_name']}")
                    st.markdown(f"**Type:** {ticket['query_type']}")
                    st.markdown(f"**Status:** {ticket['status']}")
                    st.markdown(f"**Agent:** {ticket['assigned_agent'] or 'Unassigned'}")
                    st.markdown(f"**Created:** {ticket['created_at']}")
                    st.markdown(f"**Query:** {ticket['query_text']}")
                    
                    if ticket.get('resolution_notes'):
                        st.success(f"**Resolution:** {ticket['resolution_notes']}")
        else:
            st.info("No tickets in system")
    
    with tab4:
        st.markdown("### Knowledge Base Developer Feedback")
        st.info("This feedback is from agents about KB effectiveness - use it to improve the system")
        
        kb_feedbacks = db.get_kb_feedbacks()
        
        if kb_feedbacks:
            helpfulness_scores = {
                "Very Poor": 0, "Poor": 0, "Average": 0, "Good": 0, "Excellent": 0
            }
            
            for feedback in kb_feedbacks:
                helpfulness_scores[feedback['kb_helpfulness']] += 1
            
            st.markdown("### KB Helpfulness Summary")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Very Poor", helpfulness_scores["Very Poor"])
            with col2:
                st.metric("Poor", helpfulness_scores["Poor"])
            with col3:
                st.metric("Average", helpfulness_scores["Average"])
            with col4:
                st.metric("Good", helpfulness_scores["Good"])
            with col5:
                st.metric("Excellent", helpfulness_scores["Excellent"])
            
            total_feedback = len(kb_feedbacks)
            good_feedback = helpfulness_scores["Good"] + helpfulness_scores["Excellent"]
            satisfaction_rate = (good_feedback / total_feedback * 100) if total_feedback > 0 else 0
            
            st.markdown(f"**Overall KB Satisfaction Rate:** {satisfaction_rate:.1f}%")
            
            st.markdown("---")
            st.markdown("### Detailed Agent Feedback")
            
            for feedback in kb_feedbacks:
                rating_color = "🟢" if feedback['kb_helpfulness'] in ["Good", "Excellent"] else "🟡" if feedback['kb_helpfulness'] == "Average" else "🔴"
                
                with st.expander(f"{rating_color} Ticket {feedback['ticket_id']} - {feedback['kb_helpfulness']} - {feedback['query_type']}"):
                    st.markdown(f"**Agent:** {feedback['agent_name']}")
                    st.markdown(f"**Date:** {feedback['timestamp']}")
                    st.markdown(f"**Query Type:** {feedback['query_type']}")
                    st.markdown(f"**KB Rating:** {feedback['kb_helpfulness']}")
                    
                    if feedback['kb_feedback'] and feedback['kb_feedback'] != "No additional comments":
                        st.markdown("**Agent's Improvement Suggestions:**")
                        st.warning(feedback['kb_feedback'])
                    else:
                        st.info("No KB feedback received yet")

if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.role == 'user':
        user_interface()
    elif st.session_state.role == 'agent':
        agent_interface()
    elif st.session_state.role == 'manager':
        manager_interface()