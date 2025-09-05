from services.gmail_api import authenticate_gmail, fetch_latest_emails
from services.summary import summarize_email
from services.utils import clean_text
from generate_html import save_emails

def main():
    """
    Connects to the Gmail API, fetches the latest n emails, and prints their subject, sender, and a preview of the body.
    """
    n = 5 
    service = authenticate_gmail()
    emails = fetch_latest_emails(service, n=n)

    processed = []

    for email in emails:
        body = clean_text(email['body'])
        summary = summarize_email(body)
        # print(summary) # Uncomment to see summaries in console
        processed.append({
            "subject": email["subject"],
            "sender": email["sender"],
            "summary": summary,
            "body": body
        })


        
    save_emails(processed, 'output/inbox.html')

if __name__ == "__main__":
    main()
