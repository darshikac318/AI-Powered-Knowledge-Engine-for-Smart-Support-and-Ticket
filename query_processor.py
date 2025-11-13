# src/recommendations/query_processor.py
"""
Query Processor Module
----------------------
This module cleans and analyzes customer queries before searching
the knowledge base. It removes stopwords, punctuation, and performs
lemmatization to normalize queries for better matching.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download once (safe if re-run)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class QueryProcessor:
    """Cleans and preprocesses customer queries."""

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_query(self, query: str) -> str:
        """
        Normalize query text:
        - Convert to lowercase
        - Remove special characters and digits
        - Remove stopwords
        - Lemmatize words
        """
        query = query.lower()
        query = re.sub(r'[^a-z\s]', '', query)  # keep only alphabets and spaces
        tokens = [
            self.lemmatizer.lemmatize(word)
            for word in query.split()
            if word not in self.stop_words
        ]
        return ' '.join(tokens)


# ✅ Example (run this to test)
if __name__ == "__main__":
    qp = QueryProcessor()
    sample = "How can I RESET my password quickly?"
    print("Original:", sample)
    print("Cleaned :", qp.clean_query(sample))
