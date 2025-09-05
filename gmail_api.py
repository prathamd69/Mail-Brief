from __future__ import print_function
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """
    Authenticates the user with Gmail API using OAuth2 credentials.
    Loads credentials from 'token.json' if available, otherwise initiates the OAuth flow.
    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service object.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def fetch_latest_emails(service, n=5):
    """
    Fetches the latest n emails from the user's Gmail inbox.
    Extracts subject, sender, and plain text body for each email.
    Args:
        service (googleapiclient.discovery.Resource): Authenticated Gmail API service object.
        n (int): Number of latest emails to fetch.
    Returns:
        list: List of dictionaries containing 'subject', 'sender', and 'body' for each email.
    """
    results = service.users().messages().list(userId="me", maxResults=n).execute()
    messages = results.get("messages", [])
    email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")
        body = ""
        if "parts" in msg_data["payload"]:
            for part in msg_data["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data")
                    if data:
                        body = base64.urlsafe_b64decode(data).decode("utf-8")
                        break
        else:
            data = msg_data["payload"]["body"].get("data")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8")
        email_list.append({"subject": subject, "sender": sender, "body": body})
    return email_list
