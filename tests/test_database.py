import unittest
import sqlite3
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import (
    create_connection,
    create_tables,
    add_user,
    verify_user,
    create_ticket,
    get_user_tickets,
    update_ticket_status
)


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db = "test_support_system.db"
        
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    
    def setUp(self):
        self.conn = create_connection(self.test_db)
        create_tables(self.conn)
    
    def tearDown(self):
        if self.conn:
            self.conn.close()
    
    def test_create_connection(self):
        self.assertIsNotNone(self.conn)
        self.assertIsInstance(self.conn, sqlite3.Connection)
    
    def test_create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('users', 'tickets', 'chats')
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('users', tables)
        self.assertIn('tickets', tables)
    
    def test_add_user(self):
        result = add_user(self.conn, "testuser", "password123", "customer")
        self.assertTrue(result)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", ("testuser",))
        user = cursor.fetchone()
        
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "testuser") 
        self.assertEqual(user[3], "customer")  
    
    def test_add_duplicate_user(self):
        add_user(self.conn, "testuser", "password123", "customer")
        result = add_user(self.conn, "testuser", "password456", "agent")
        
        self.assertFalse(result)
    
    def test_verify_user_success(self):
        add_user(self.conn, "testuser", "password123", "customer")
        user = verify_user(self.conn, "testuser", "password123")
        
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['role'], "customer")
    
    def test_verify_user_wrong_password(self):
        add_user(self.conn, "testuser", "password123", "customer")
        user = verify_user(self.conn, "testuser", "wrongpassword")
        
        self.assertIsNone(user)
    
    def test_verify_user_nonexistent(self):
        user = verify_user(self.conn, "nonexistent", "password")
        self.assertIsNone(user)
    
    def test_create_ticket(self):
        add_user(self.conn, "customer1", "pass123", "customer")
        
        ticket_id = create_ticket(
            self.conn,
            customer_name="John Doe",
            customer_username="customer1",
            order_id="ORD12345",
            issue_description="Product not delivered"
        )
        
        self.assertIsNotNone(ticket_id)
        self.assertTrue(ticket_id.startswith("TKT"))
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        ticket = cursor.fetchone()
        
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket[2], "John Doe") 
        self.assertEqual(ticket[4], "ORD12345")  
    
    def test_get_user_tickets(self):
        add_user(self.conn, "customer1", "pass123", "customer")
        ticket1 = create_ticket(self.conn, "John Doe", "customer1", "ORD1", "Issue 1")
        ticket2 = create_ticket(self.conn, "John Doe", "customer1", "ORD2", "Issue 2")
        
        tickets = get_user_tickets(self.conn, "customer1")
        
        self.assertEqual(len(tickets), 2)
        ticket_ids = [t['ticket_id'] for t in tickets]
        self.assertIn(ticket1, ticket_ids)
        self.assertIn(ticket2, ticket_ids)
    
    def test_update_ticket_status(self):
        add_user(self.conn, "customer1", "pass123", "customer")
        add_user(self.conn, "agent1", "pass123", "agent")
        
        ticket_id = create_ticket(self.conn, "John Doe", "customer1", "ORD1", "Issue")
        
        result = update_ticket_status(
            self.conn,
            ticket_id,
            "In Progress",
            assigned_agent="agent1"
        )
        
        self.assertTrue(result)
        cursor = self.conn.cursor()
        cursor.execute("SELECT status, assigned_agent FROM tickets WHERE ticket_id = ?", 
                      (ticket_id,))
        row = cursor.fetchone()
        
        self.assertEqual(row[0], "In Progress")
        self.assertEqual(row[1], "agent1")
    
    def test_ticket_status_workflow(self):
        add_user(self.conn, "customer1", "pass123", "customer")
        add_user(self.conn, "agent1", "pass123", "agent")
        ticket_id = create_ticket(self.conn, "John Doe", "customer1", "ORD1", "Issue")
        tickets = get_user_tickets(self.conn, "customer1")
        self.assertEqual(tickets[0]['status'], "Open")
        
        update_ticket_status(self.conn, ticket_id, "In Progress", "agent1")
        tickets = get_user_tickets(self.conn, "customer1")
        self.assertEqual(tickets[0]['status'], "In Progress")

        update_ticket_status(self.conn, ticket_id, "Resolved", "agent1", "Issue resolved successfully")
        tickets = get_user_tickets(self.conn, "customer1")
        self.assertEqual(tickets[0]['status'], "Resolved")
        self.assertIsNotNone(tickets[0].get('resolution_notes'))

def run_tests():
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()