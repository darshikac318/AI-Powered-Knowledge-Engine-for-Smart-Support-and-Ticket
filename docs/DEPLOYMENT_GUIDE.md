# Deployment Guide

## Option 1: Local Deployment

### Step 1: Prepare Environment
```bash
# Install Python 3.10+
python --version

# Install pip
pip --version
```

### Step 2: Install Application
```bash
# Extract project files
cd AI-Powered-Knowledge-Engine-for-Smart-Support-and-Ticket

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Build Knowledge Base
```bash
# Ensure 13 PDFs in data/raw/
python load_knowledge_base.py
```

### Step 4: Run Application
```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## Option 2: Network Deployment

### Allow Network Access
```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Access from other computers:
```
http://[YOUR_IP]:8501
```

Find your IP:
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

---

## Option 3: Cloud Deployment (Streamlit Cloud - FREE)

### Prerequisites

- GitHub account
- Code pushed to GitHub repository

### Steps

1. **Push to GitHub**
```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin [your-repo-url]
   git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to: https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Deploy"

3. **Configure**
   - Wait for deployment (2-5 minutes)
   - Get public URL
   - Share with users

### Important Notes

- Free tier includes 1GB storage
- Database persists on cloud
- Knowledge base needs to be built after deployment
- Add `load_knowledge_base.py` to startup if needed

---

## Troubleshooting Deployment

### Issue: Module Not Found
```bash
pip install -r requirements.txt
```

### Issue: Port Already in Use
```bash
# Change port
streamlit run app.py --server.port=8502
```

### Issue: Knowledge Base Missing
```bash
python load_knowledge_base.py
```

### Issue: Database Error
```bash
# Delete and recreate
rm data/support_system.db
streamlit run app.py
```

---

## Post-Deployment Checklist

- [ ] Application accessible
- [ ] Login works for all roles
- [ ] Tickets can be created
- [ ] Knowledge base search works
- [ ] Chat functionality works
- [ ] Database persists data
- [ ] All 13 PDFs loaded

---

## Maintenance

### Update Application
```bash
git pull origin main
pip install -r requirements.txt --upgrade
streamlit run app.py
```

### Backup Before Updates
```bash
cp data/support_system.db data/backups/backup_before_update.db
```

---

## System Requirements

### Minimum

- CPU: 2 cores
- RAM: 4GB
- Disk: 5GB
- OS: Windows 10/Mac/Linux

### Recommended

- CPU: 4 cores
- RAM: 8GB
- Disk: 10GB
- OS: Windows 11/Mac/Ubuntu

Version: 1.0