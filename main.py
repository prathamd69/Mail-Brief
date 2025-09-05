from gmail_api import authenticate_gmail, fetch_latest_emails

def main():
    """
    Connects to the Gmail API, fetches the latest 5 emails, and prints their subject, sender, and a preview of the body.
    """
    service = authenticate_gmail()
    emails = fetch_latest_emails(service, n=5)
    for idx, email in enumerate(emails, 1):
        print(f"\n[{idx}]  Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        body_preview = email['body'][:200].replace("\n", " ")
        print(f"    Body Preview: {body_preview}...\n")

if __name__ == "__main__":
    main()
