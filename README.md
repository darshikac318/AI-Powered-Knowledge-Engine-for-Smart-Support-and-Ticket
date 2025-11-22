# Amazon Knowledge Support System

AI-Powered Knowledge Engine for Smart Support and Ticket Resolution

## Overview

This system provides intelligent customer support for Amazon Returns and Replacements queries using AI-powered semantic search and vector databases.

## Features

- **Role-Based Access Control**: Separate interfaces for Customers, Support Agents, and Content Managers
- **AI-Powered Search**: Semantic search using Sentence Transformers and ChromaDB
- **Real-Time Chat**: Customer-Agent communication system
- **Knowledge Base**: 13 Amazon policy documents with 41 semantic chunks
- **Ticket Management**: Complete ticket lifecycle tracking
- **Analytics Dashboard**: Performance metrics and KB feedback analysis
- **Privacy-Focused**: Minimal data collection (no email/phone storage)

## Quick Start

### Prerequisites

- Python 3.10 or higher
- 8GB RAM minimum
- 5GB disk space

### Installation
```bash
# Clone repository
git clone [repository-url]
cd AI-Powered-Knowledge-Engine-for-Smart-Support-and-Ticket

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Build Knowledge Base
```bash
# Ensure 13 PDF files are in data/raw/ folder
python load_knowledge_base.py
```

Expected output:
```
Found 13 PDF files
Processing...
Total chunks: 41
Build Complete
```

### Run Application
```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

## Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Customer | user1 | user123 |
| Support Agent | agent1 | agent123 |
| Content Manager | manager1 | manager123 |

## System Architecture
```
Frontend: Streamlit (Python)
Backend: SQLite Database
Knowledge Base: ChromaDB (Vector Database)
Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
Search Method: Semantic Similarity (Cosine)
```

## Project Structure
```
├── app.py                          # Main Streamlit application
├── database.py                     # Database management
├── load_knowledge_base.py          # KB builder
├── src/
│   ├── data_ingestion/             # PDF processing
│   ├── recommendations/            # Search & recommendations
|   ├── integrations/               # Integration
│   ├── analytics/                  # Metrics & reports
│   ├── backup/                     # Backup management
│   └── monitoring/                 # Performance tracking
├── docs/                           # Documentation
├── tests/                          # Test suite
└── data/
    ├── raw/                        # Source PDFs
    ├── processed/                  # ChromaDB
    └── support_system.db           # SQLite database
```

## Usage

### For Customers

1. Login with user credentials
2. Go to "Raise Query" tab
3. Fill form and submit ticket
4. Use "Support Chat" to communicate with agent
5. Check "My Tickets" for status and resolution

### For Support Agents

1. Login with agent credentials
2. View "Ticket Queue" for open tickets
3. Click "Handle Ticket" to start working
4. Use "Knowledge Base Search" to find solutions
5. Chat with customer in "Active Chats"
6. Provide resolution notes and KB feedback
7. Click "Resolve Ticket" when done

### For Content Managers

1. Login with manager credentials
2. View "Knowledge Base Stats" for system info
3. Check "Ticket Analytics" for metrics
4. Review "All Tickets" for complete overview
5. Read "KB Developer Feedback" to improve system

## Technology Stack

- **Frontend**: Streamlit 1.28.0
- **Database**: SQLite3
- **Vector DB**: ChromaDB 0.4.18
- **Embeddings**: Sentence Transformers 2.2.2
- **NLP**: NLTK 3.8.1, Transformers 4.35.0
- **PDF Processing**: PyPDF2, PDFPlumber, PyMuPDF
- **Analytics**: Pandas, Matplotlib, Seaborn

## Features in Detail

### Semantic Search
- Converts queries to 384-dimensional vectors
- Searches 41 knowledge chunks using cosine similarity
- Returns top 5 most relevant solutions with relevance scores

### Ticket System
- Unique ticket IDs (TKT12345)
- Status tracking: Open → In Progress → Resolved
- Agent assignment
- Resolution notes for customers

### Feedback System
- Two-tier feedback:
  - Customer resolution notes (visible to customer)
  - KB effectiveness feedback (visible to managers only)
- KB helpfulness ratings (Very Poor to Excellent)
- Improvement suggestions from agents

### Privacy Protection
- Only stores: Name, Order ID, Issue Description
- No email or phone collection
- Minimal data retention
- Secure session management

## Performance Metrics

- Search Response Time: < 2 seconds
- Knowledge Base Size: 50MB
- Database Size: ~5MB
- Concurrent Users: 10-20 supported
- Accuracy: 85-90% relevance for standard queries

## Testing

Run test suite:
```bash
python -m pytest tests/
```

Test individual components:
```bash
python tests/test_knowledge_base.py
python tests/test_recommendations.py
python tests/test_database.py
```

## Deployment

### Local Network
```bash
streamlit run app.py --server.address=0.0.0.0
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy from repository
4. Access via public URL

See `docs/DEPLOYMENT_GUIDE.md` for detailed instructions.

## Documentation

- **User Manual**: `docs/USER_MANUAL.md`
- **Admin Guide**: `docs/ADMIN_GUIDE.md`
- **Technical Docs**: `docs/TECHNICAL_DOCUMENTATION.md`
- **Deployment**: `docs/DEPLOYMENT_GUIDE.md`

## Troubleshooting

### Knowledge Base Not Found
```bash
python load_knowledge_base.py
```

### Module Import Errors
```bash
pip install -r requirements.txt
```

### Database Locked
```bash
# Close all connections and restart
streamlit run app.py
```

### Port Already in Use

streamlit run app.py --server.port=8502

## Maintenance

### Daily
- Monitor system logs
- Check disk space
- Verify application running

### Weekly
- Backup database
- Review KB feedback
- Check performance metrics

### Monthly
- Update knowledge base
- System health check
- Security audit

## Backup

Manual backup:
cp data/support_system.db data/backups/backup_$(date +%Y%m%d).db

Automated backup available via `src/backup/backup_manager.py`

## Contributing

Team Members:
- **Taruni**: Data Engineering & Backup Systems
- **Nandani**: AI/ML & Recommendation Engine
- **Nimisha**: Analytics & Reporting
- **Darshika**: Integration & Infrastructure

## License

Internal Project - Educational Use Only

## Support

For technical support or questions, contact the development team.

## Changelog

### Version 1.0 (November 2025)
- Initial release
- 3 role-based interfaces
- 13 PDF knowledge base
- Semantic search
- Ticket management
- Chat functionality
- Analytics dashboard
- KB feedback system

## Acknowledgments

- Sentence Transformers for embeddings
- ChromaDB for vector database
- Streamlit for rapid UI development

**Amazon Knowledge Support System v1.0**
Built with ❤️ for efficient customer support
