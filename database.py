import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data/support_system.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                order_id TEXT,
                query_type TEXT NOT NULL,
                query_text TEXT NOT NULL,
                status TEXT DEFAULT 'Open',
                assigned_agent TEXT,
                resolution_notes TEXT,
                created_at TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kb_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                query_type TEXT,
                kb_helpfulness TEXT,
                kb_feedback TEXT,
                agent_name TEXT,
                timestamp TEXT,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        ''')

        try:
            self.cursor.execute("""
                INSERT INTO users (username, password, role) 
                VALUES ('user1', 'user123', 'user')
            """)
        except:
            pass
        
        try:
            self.cursor.execute("""
                INSERT INTO users (username, password, role) 
                VALUES ('agent1', 'agent123', 'agent')
            """)
        except:
            pass
        
        try:
            self.cursor.execute("""
                INSERT INTO users (username, password, role) 
                VALUES ('manager1', 'manager123', 'manager')
            """)
        except:
            pass
        
        self.conn.commit()
        
        self.migrate_tickets_table()
        self.ensure_timestamps_in_tickets()
    
    def get_ist_timestamp(self):
        utc_now = datetime.utcnow()
        ist_now = utc_now + timedelta(hours=5, minutes=30)
        return ist_now.strftime("%Y-%m-%d %H:%M:%S")
    
    def migrate_tickets_table(self):
        try:
            self.cursor.execute("ALTER TABLE tickets ADD COLUMN customer_username TEXT")
            self.cursor.execute("""
                UPDATE tickets 
                SET customer_username = 'user1' 
                WHERE customer_username IS NULL
            """)
            self.conn.commit()
        except:
            pass  

    def ensure_timestamps_in_tickets(self):
        try:
            self.cursor.execute("ALTER TABLE tickets ADD COLUMN updated_at TEXT")
            self.conn.commit()
        except:
            pass
    
    def authenticate_user(self, username, password):
        self.cursor.execute("""
            SELECT role FROM users 
            WHERE username = ? AND password = ?
        """, (username, password))
        
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_tickets(self, status=None, username=None):
        if username:
            if status:
                self.cursor.execute("""
                    SELECT * FROM tickets 
                    WHERE customer_username = ? AND status = ?
                    ORDER BY created_at DESC
                """, (username, status))
            else:
                self.cursor.execute("""
                    SELECT * FROM tickets 
                    WHERE customer_username = ?
                    ORDER BY created_at DESC
                """, (username,))
        elif status:
            self.cursor.execute("""
                SELECT * FROM tickets 
                WHERE status = ?
                ORDER BY created_at DESC
            """, (status,))
        else:
            self.cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
        
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def create_ticket(self, ticket_data):
        ticket_data['created_at'] = self.get_ist_timestamp()
        
        self.cursor.execute("""
            INSERT INTO tickets 
            (ticket_id, customer_name, customer_username, order_id, 
             query_type, query_text, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_data['ticket_id'],
            ticket_data['customer_name'],
            ticket_data.get('customer_username'),
            ticket_data.get('order_id', ''),
            ticket_data['query_type'],
            ticket_data['query_text'],
            ticket_data['status'],
            ticket_data['created_at']
        ))
        
        self.conn.commit()
    
    def update_ticket_status(self, ticket_id, status):
        timestamp = self.get_ist_timestamp()
        
        self.cursor.execute("""
            UPDATE tickets 
            SET status = ?, updated_at = ?
            WHERE ticket_id = ?
        """, (status, timestamp, ticket_id))
        
        if status == 'Resolved':
            self.cursor.execute("""
                DELETE FROM chats WHERE ticket_id = ?
            """, (ticket_id,))
        
        self.conn.commit()
    
    def assign_agent(self, ticket_id, agent_name):
        self.cursor.execute("""
            UPDATE tickets 
            SET assigned_agent = ? 
            WHERE ticket_id = ?
        """, (agent_name, ticket_id))
        
        self.conn.commit()
    
    def add_resolution_notes(self, ticket_id, notes):
        self.cursor.execute("""
            UPDATE tickets 
            SET resolution_notes = ? 
            WHERE ticket_id = ?
        """, (notes, ticket_id))
        
        self.conn.commit()
    
    def add_chat_message(self, ticket_id, sender, message):
        """Add a chat message with IST timestamp"""
        timestamp = self.get_ist_timestamp()
        
        self.cursor.execute("""
            INSERT INTO chats (ticket_id, sender, message, timestamp)
            VALUES (?, ?, ?, ?)
        """, (ticket_id, sender, message, timestamp))
        
        self.conn.commit()

    def get_chat_messages(self, ticket_id):
        self.cursor.execute("""
            SELECT * FROM chats 
            WHERE ticket_id = ? 
            ORDER BY timestamp ASC
        """, (ticket_id,))
        
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def add_kb_feedback(self, feedback_data):
        self.cursor.execute("""
            INSERT INTO kb_feedback 
            (ticket_id, query_type, kb_helpfulness, kb_feedback, agent_name, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            feedback_data['ticket_id'],
            feedback_data['query_type'],
            feedback_data['kb_helpfulness'],
            feedback_data['kb_feedback'],
            feedback_data['agent_name'],
            feedback_data['timestamp']
        ))
        
        self.conn.commit()

    def get_kb_feedbacks(self):
        self.cursor.execute("""
            SELECT * FROM kb_feedback 
            ORDER BY timestamp DESC
        """)
        
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]