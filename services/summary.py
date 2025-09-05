from transformers import pipeline

summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn",framework="pt")

def summarize_email(text):
    if not text:
        return "No content"
    try:
        summary = summarizer_pipeline(text, max_length=80, min_length=20, do_sample=False)
        return summary[0]['summary_text']
    
    except Exception as e:
        return f"[Summarization failed: {e}]"
