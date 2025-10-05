import os.path
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/drive.file"]

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = BASE_DIR / "credentials.json"
TOKEN_PATH = BASE_DIR / "token.json"


def authenticate_gmail():
    """
    Authenticates the user with Gmail API using OAuth2 credentials.
    Loads credentials from 'token.json' if available, otherwise initiates the OAuth flow.
    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service object.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(str(TOKEN_PATH), "w") as token:
            token.write(creds.to_json())

    return creds

def create_service():
    """
    Creates a Gmail API service object.
    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service object.
    """
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)
    return service
