import re

class QueryProcessor:
    def __init__(self):
        self.intent_keywords = {
            'return': ['return', 'send back', 'give back'],
            'refund': ['refund', 'money back', 'reimbursement'],
            'replacement': ['replace', 'exchange', 'swap'],
            'damaged': ['damaged', 'broken', 'defective']
        }

    def clean_query(self, query: str) -> str:
        query = query.lower().strip()
        query = re.sub(r'[^\w\s]', '', query)
        query = re.sub(r'\s+', ' ', query)
        return query

    def detect_intent(self, query: str) -> str:
        query_lower = query.lower()
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        return 'general'

    def process_query(self, raw_query: str):
        cleaned = self.clean_query(raw_query)
        intent = self.detect_intent(cleaned)
 
        return {
            'original': raw_query,
            'cleaned': cleaned,
            'intent': intent
        }