from services.read_emails import init_gmail_service, get_email_details, get_email_content
from utilities.upload import upload_to_drive
from googleapiclient.discovery import build
from config import DRIVE_FOLDER_ID
import json


def main(max_emails=10):
    OUTPUT_FILE = "emails.json"
 
    gmail_service = init_gmail_service()
    creds = gmail_service._http.credentials

    drive_service = build('drive', 'v3', credentials=creds)

    email_data = get_email_details(gmail_service, folder_name='Inbox', max_results=max_emails)
    all_emails = []

    for email in email_data:
        details = get_email_content(gmail_service, email['id'])
        if details:
            all_emails.append(details)

    print(f"✅ Fetched {len(all_emails)} emails")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_emails, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(all_emails)} emails to {OUTPUT_FILE}")

    upload_to_drive(drive_service, OUTPUT_FILE, folder_id=DRIVE_FOLDER_ID)