import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path="data/support_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                order_id TEXT,
                query_type TEXT NOT NULL,
                query_text TEXT NOT NULL,
                status TEXT DEFAULT 'Open',
                created_at TIMESTAMP,
                assigned_agent TEXT,
                resolution_notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kb_feedbacks (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                query_type TEXT NOT NULL,
                kb_helpfulness TEXT NOT NULL,
                kb_feedback TEXT,
                agent_name TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        ''')
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, role) 
            VALUES ('user1', 'user123', 'user')
        ''')
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, role) 
            VALUES ('agent1', 'agent123', 'agent')
        ''')
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, role) 
            VALUES ('manager1', 'manager123', 'manager')
        ''')
        
        conn.commit()
        conn.close()
    
    def authenticate_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def create_ticket(self, ticket_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets (ticket_id, customer_name, order_id, query_type, query_text, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            ticket_data['ticket_id'],
            ticket_data['customer_name'],
            ticket_data.get('order_id', ''),
            ticket_data['query_type'],
            ticket_data['query_text'],
            ticket_data['status'],
            ticket_data['created_at']
        ))
        conn.commit()
        conn.close()
    
    def get_tickets(self, status=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if status:
            cursor.execute("SELECT * FROM tickets WHERE status=? ORDER BY created_at DESC", (status,))
        else:
            cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
        
        columns = [description[0] for description in cursor.description]
        tickets = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return tickets
    
    def update_ticket_status(self, ticket_id, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET status=? WHERE ticket_id=?", (status, ticket_id))
        conn.commit()
        conn.close()
    
    def assign_agent(self, ticket_id, agent_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET assigned_agent=? WHERE ticket_id=?", (agent_name, ticket_id))
        conn.commit()
        conn.close()
    
    def add_resolution_notes(self, ticket_id, resolution_notes):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET resolution_notes=? WHERE ticket_id=?", (resolution_notes, ticket_id))
        conn.commit()
        conn.close()
    
    def add_chat_message(self, ticket_id, sender, message):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_messages (ticket_id, sender, message) VALUES (?, ?, ?)",
            (ticket_id, sender, message)
        )
        conn.commit()
        conn.close()
    
    def get_chat_messages(self, ticket_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sender, message, timestamp FROM chat_messages WHERE ticket_id=? ORDER BY timestamp",
            (ticket_id,)
        )
        messages = [
            {'sender': row[0], 'message': row[1], 'timestamp': row[2]}
            for row in cursor.fetchall()
        ]
        conn.close()
        return messages
    
    def add_kb_feedback(self, feedback_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO kb_feedbacks (ticket_id, query_type, kb_helpfulness, kb_feedback, agent_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            feedback_data['ticket_id'],
            feedback_data['query_type'],
            feedback_data['kb_helpfulness'],
            feedback_data['kb_feedback'],
            feedback_data['agent_name']
        ))
        conn.commit()
        conn.close()
    
    def get_kb_feedbacks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kb_feedbacks ORDER BY timestamp DESC")
        
        columns = [description[0] for description in cursor.description]
        feedbacks = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return feedbacks