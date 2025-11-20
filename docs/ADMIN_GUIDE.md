# Admin Guide - Amazon Knowledge Support System

## System Setup

### Prerequisites
```bash
Python 3.10 or higher
pip package manager
8GB RAM minimum
5GB disk space
```

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

### Building Knowledge Base
```bash
# Place 13 PDF files in data/raw/ folder
# Run knowledge base builder
python load_knowledge_base.py
```

Expected output:
```
Found 13 PDF files
Processing: [PDF name]
...
Total chunks: 41
Build Complete
```

### Starting Application
```bash
streamlit run app.py
```

Application opens at: `http://localhost:8501`

---

## Database Management

### Database Location
```
data/support_system.db
```

### Tables

1. **users** - User accounts (user, agent, manager)
2. **tickets** - Customer support tickets
3. **chat_messages** - Conversation history
4. **kb_feedbacks** - Knowledge base effectiveness feedback

### Backup Database
```bash
# Manual backup
cp data/support_system.db data/backups/backup_[date].db
```

### Reset Database
```bash
# Delete existing database
rm data/support_system.db

# Restart application (auto-creates new database)
streamlit run app.py
```

---

## User Management

### Default Users
```
Customer: user1 / user123
Agent: agent1 / agent123
Manager: manager1 / manager123
```

### Adding New Users

Connect to database:
```bash
sqlite3 data/support_system.db
```

Add user:
```sql
INSERT INTO users (username, password, role) 
VALUES ('username', 'password', 'user');
-- role can be: 'user', 'agent', or 'manager'
```

---

## Monitoring

### System Health

Check:
- Database size: `data/support_system.db`
- ChromaDB size: `data/processed/`
- Memory usage: Task Manager/Activity Monitor
- Disk space

### Performance Logs

Located at: `data/performance_logs.json`

Contains:
- Search response times
- Ticket operations
- System metrics

---

## Troubleshooting

### Knowledge Base Not Found

Error: "Knowledge base not loaded"

Solution:
```bash
python load_knowledge_base.py
```

### Database Locked

Error: "database is locked"

Solution:
- Close all database connections
- Restart application

### Memory Issues

Error: High memory usage

Solution:
- Restart application
- Clear browser cache
- Check for memory leaks

### Import Errors

Error: "No module named..."

Solution:
```bash
pip install -r requirements.txt
```

---

## Maintenance

### Daily Tasks

- Check system logs
- Monitor disk space
- Verify application is running

### Weekly Tasks

- Backup database
- Review KB feedback
- Check performance metrics

### Monthly Tasks

- Update knowledge base if needed
- Clean old performance logs
- System health check

---

## Security

### Best Practices

- Change default passwords
- Regular backups
- Monitor user access
- Keep software updated

### Data Privacy

- Only store necessary data
- No email/phone in database
- Secure database file
- Regular security audits

---

## Configuration

### Update Port

Edit `.streamlit/config.toml`:
```toml
[server]
port = 8501
```

### Update Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF9900"
backgroundColor = "#FFFFFF"
```

---

## Support

For technical support, contact development team.

Version: 1.0
System: Amazon Knowledge Support