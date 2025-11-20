# Technical Documentation

## System Architecture
```
Frontend: Streamlit (Python)
Backend: SQLite Database
Knowledge Base: ChromaDB (Vector Database)
Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
Search: Semantic Similarity
```

## Components

### 1. Data Ingestion
- **File**: `src/data_ingestion/pdf_processor.py`
- **Function**: Extract text from PDFs, semantic chunking
- **Output**: 41 semantic chunks from 13 PDFs

### 2. Embedding Generation
- **File**: `src/embedding_generator.py`
- **Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Function**: Convert text to vector embeddings

### 3. Vector Database
- **File**: `src/integrations/chroma_db.py`
- **Technology**: ChromaDB
- **Function**: Store and search embeddings

### 4. Recommendation Engine
- **File**: `src/recommendations/recommendation_engine.py`
- **Function**: Search knowledge base, return top results
- **Method**: Cosine similarity

### 5. User Interface
- **File**: `app.py`
- **Technology**: Streamlit
- **Roles**: User, Agent, Manager

### 6. Database
- **File**: `database.py`
- **Technology**: SQLite
- **Tables**: users, tickets, chat_messages, kb_feedbacks

## Data Flow
```
User Query → Query Processor → Embedding Generator
           → ChromaDB Search → Similarity Ranking
           → Top 5 Results → Agent Interface
```

## API Reference

### Database Class
```python
db = Database()

# Authentication
role = db.authenticate_user(username, password)

# Tickets
db.create_ticket(ticket_data)
tickets = db.get_tickets(status='Open')
db.update_ticket_status(ticket_id, 'Resolved')

# Chat
db.add_chat_message(ticket_id, sender, message)
messages = db.get_chat_messages(ticket_id)

# Feedback
db.add_kb_feedback(feedback_data)
feedbacks = db.get_kb_feedbacks()
```

### RecommendationEngine Class
```python
from recommendations.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()
results = engine.get_recommendations(query, top_k=5)

# Returns:
{
    'query_info': {...},
    'recommendations': [...],
    'total_found': int
}
```

## Performance Metrics

- **Search Response Time**: < 2 seconds
- **Database Size**: ~5MB
- **ChromaDB Size**: ~50MB
- **Concurrent Users**: 10-20

## Security

- Password stored in plaintext (demo only)
- No encryption (demo only)
- Session-based authentication
- Role-based access control

**Production recommendations:**
- Hash passwords (bcrypt)
- Use HTTPS
- Implement JWT tokens
- Add rate limiting

## Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Connect GitHub to Streamlit Cloud
3. Deploy from repository
4. Configure secrets (if needed)

## Limitations

- No real-time chat (requires manual refresh)
- No email notifications
- Single-server only
- Demo authentication only

## Future Improvements

- WebSocket for real-time chat
- Email notifications for tickets
- Multi-language support
- Advanced analytics dashboard
- API endpoints for integration

Version: 1.0