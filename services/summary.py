def summarize_email(text):
    """
    Dummy summarizer for now.
    
    """
    if not text:
        return "No content"
    
    # Simple heuristic: first 2 sentences
    sentences = text.split(". ")
    summary = ". ".join(sentences[:2])
    return summary.strip() + ("..." if len(sentences) > 2 else "")
