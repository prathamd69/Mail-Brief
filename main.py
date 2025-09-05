from services.gmail_api import authenticate_gmail, fetch_latest_emails
from services.summary import summarize_email
from services.utils import clean_text

def main():
    """
    Connects to the Gmail API, fetches the latest 5 emails, and prints their subject, sender, and a preview of the body.
    """
    service = authenticate_gmail()
    emails = fetch_latest_emails(service, n=5)

    processed = []

    for email in emails:
        body = clean_text(email['body'])
        summary = summarize_email(body)
        processed.append({
            "subject": email["subject"],
            "sender": email["sender"],
            "body": summary
        })
    
    for email in processed:
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        print(f"Preview: {email['body']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
