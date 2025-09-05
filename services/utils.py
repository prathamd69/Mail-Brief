import re

"""
    Cleans the input email text by removing quoted replies, URLs, excessive whitespace,
    and common signature phrases.

    Args:
        text (str): The email body text to clean.

    Returns:
        str: The cleaned text.
"""

def clean_text(text):
    
    if not text:
        return ""
    
    text = re.sub(r"On .* wrote:", "", text, flags=re.DOTALL)

    text = re.sub(r"(?m)^>.*", "", text)
    
    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    text = re.sub(r"(Thanks|Regards|Best),.*", "", text, flags=re.IGNORECASE)

    return text