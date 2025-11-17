# text_cleaner.py
import re

def clean_text(text: str) -> str:
    """
    Clean the input text by:
    - Lowercasing
    - Removing special characters
    - Stripping extra spaces
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
<<<<<<< HEAD
    return text.strip()
=======
    return text.strip()
>>>>>>> cbc81c9cf4a0e207fdcc3fec1ef612c4bdff58d4
