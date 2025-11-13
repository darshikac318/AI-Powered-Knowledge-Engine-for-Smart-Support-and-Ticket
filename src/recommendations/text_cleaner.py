# text_cleaner.py
import re

def clean_text(text):
    """
    Function to clean input text.
    Removes special characters, extra spaces, and converts to lowercase.
    """
    text = text.lower()  # lowercase
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove punctuation/special chars
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    text = text.strip()  # remove leading/trailing spaces
    return text

# Example usage
if __name__ == "__main__":
    sample_text = "Hello, Amazon Support!  This   is a Test..."
    cleaned = clean_text(sample_text)
    print("Original:", sample_text)
    print("Cleaned :", cleaned)
