import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class QueryProcessor:
    """Simple query processor for testing"""
    
    @staticmethod
    def clean_query(query: str) -> str:
        """Clean and normalize query text"""
        if not query:
            return ""
        
        # Convert to lowercase
        query = query.lower().strip()
        
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        return query
    
    @staticmethod
    def extract_keywords(query: str) -> list:
        """Extract keywords from query"""
        # Simple keyword extraction (split on spaces)
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'what', 'how', 'when'}
        
        words = query.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    @staticmethod
    def is_question(query: str) -> bool:
        """Check if query is a question"""
        query = query.strip()
        return query.endswith('?') or any(
            query.lower().startswith(q) 
            for q in ['what', 'how', 'when', 'where', 'why', 'who', 'can', 'is', 'do', 'does']
        )
    
    @staticmethod
    def categorize_query(query: str) -> str:
        """Categorize query type"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['return', 'refund', 'money back']):
            return 'returns'
        elif any(word in query_lower for word in ['shipping', 'delivery', 'tracking']):
            return 'shipping'
        elif any(word in query_lower for word in ['replace', 'replacement', 'defective']):
            return 'replacement'
        elif any(word in query_lower for word in ['account', 'login', 'password']):
            return 'account'
        else:
            return 'general'


class TestQueryProcessor(unittest.TestCase):
    """Test cases for query processor"""
    
    def setUp(self):
        """Set up before each test"""
        self.processor = QueryProcessor()
    
    def test_clean_query_whitespace(self):
        """Test query cleaning removes extra whitespace"""
        query = "  How   do   I   return   a   product?  "
        cleaned = self.processor.clean_query(query)
        
        self.assertEqual(cleaned, "how do i return a product?")
        self.assertNotIn("  ", cleaned)
    
    def test_clean_query_lowercase(self):
        """Test query cleaning converts to lowercase"""
        query = "WHAT IS THE RETURN POLICY?"
        cleaned = self.processor.clean_query(query)
        
        self.assertEqual(cleaned, "what is the return policy?")
        self.assertTrue(cleaned.islower())
    
    def test_clean_query_empty(self):
        """Test handling of empty query"""
        self.assertEqual(self.processor.clean_query(""), "")
        self.assertEqual(self.processor.clean_query("   "), "")
        self.assertEqual(self.processor.clean_query(None), "")
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction"""
        query = "How do I return a product?"
        keywords = self.processor.extract_keywords(query)
        
        self.assertIn("return", keywords)
        self.assertIn("product", keywords)
        self.assertNotIn("how", keywords)  # Stop word
        self.assertNotIn("do", keywords)   # Stop word
        self.assertNotIn("a", keywords)    # Stop word
    
    def test_extract_keywords_no_stopwords(self):
        """Test keyword extraction removes stop words"""
        query = "the product is defective"
        keywords = self.processor.extract_keywords(query)
        
        self.assertNotIn("the", keywords)
        self.assertNotIn("is", keywords)
        self.assertIn("product", keywords)
        self.assertIn("defective", keywords)
    
    def test_extract_keywords_empty(self):
        """Test keyword extraction with empty query"""
        keywords = self.processor.extract_keywords("")
        self.assertEqual(keywords, [])
    
    def test_is_question_with_question_mark(self):
        """Test question detection with question mark"""
        self.assertTrue(self.processor.is_question("Where is my order?"))
        self.assertTrue(self.processor.is_question("Can I return this?"))
    
    def test_is_question_without_question_mark(self):
        """Test question detection by starting word"""
        self.assertTrue(self.processor.is_question("How do I return"))
        self.assertTrue(self.processor.is_question("What is the policy"))
        self.assertTrue(self.processor.is_question("Can you help me"))
    
    def test_is_not_question(self):
        """Test non-question detection"""
        self.assertFalse(self.processor.is_question("I want to return this"))
        self.assertFalse(self.processor.is_question("Need help with order"))
    
    def test_categorize_query_returns(self):
        """Test categorization of return queries"""
        queries = [
            "How do I return a product?",
            "I want a refund",
            "Can I get my money back?"
        ]
        
        for query in queries:
            category = self.processor.categorize_query(query)
            self.assertEqual(category, 'returns')
    
    def test_categorize_query_shipping(self):
        """Test categorization of shipping queries"""
        queries = [
            "Where is my delivery?",
            "Tracking number not working",
            "How long does shipping take?"
        ]
        
        for query in queries:
            category = self.processor.categorize_query(query)
            self.assertEqual(category, 'shipping')
    
    def test_categorize_query_replacement(self):
        """Test categorization of replacement queries"""
        queries = [
            "Product is defective",
            "I need a replacement",
            "Can I replace this item?"
        ]
        
        for query in queries:
            category = self.processor.categorize_query(query)
            self.assertEqual(category, 'replacement')
    
    def test_categorize_query_account(self):
        """Test categorization of account queries"""
        queries = [
            "Can't login to my account",
            "Forgot my password",
            "How do I update account info?"
        ]
        
        for query in queries:
            category = self.processor.categorize_query(query)
            self.assertEqual(category, 'account')
    
    def test_categorize_query_general(self):
        """Test categorization of general queries"""
        query = "What are your business hours?"
        category = self.processor.categorize_query(query)
        self.assertEqual(category, 'general')
    
    def test_query_preprocessing_pipeline(self):
        """Test complete query preprocessing pipeline"""
        raw_query = "  HOW   DO   I   RETURN   A   DEFECTIVE   PRODUCT?  "
        
        # Clean
        cleaned = self.processor.clean_query(raw_query)
        self.assertEqual(cleaned, "how do i return a defective product?")
        
        # Extract keywords
        keywords = self.processor.extract_keywords(cleaned)
        self.assertIn("return", keywords)
        self.assertIn("defective", keywords)
        self.assertIn("product", keywords)
        
        # Check if question
        is_q = self.processor.is_question(cleaned)
        self.assertTrue(is_q)
        
        # Categorize
        category = self.processor.categorize_query(cleaned)
        self.assertEqual(category, "returns")
    
    def test_special_characters_handling(self):
        """Test handling of special characters"""
        queries = [
            "What's the return policy?",
            "Can I return this (opened box)?",
            "Order #12345 - where is it?"
        ]
        
        for query in queries:
            cleaned = self.processor.clean_query(query)
            # Should not crash and should return something
            self.assertIsNotNone(cleaned)
            self.assertIsInstance(cleaned, str)
    
    def test_multilingual_query_handling(self):
        """Test basic handling of non-English characters"""
        # This is a simple test - in production you'd want proper i18n
        query = "café return policy"
        cleaned = self.processor.clean_query(query)
        
        # Should handle without crashing
        self.assertIsNotNone(cleaned)
        self.assertIn("café", cleaned)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()