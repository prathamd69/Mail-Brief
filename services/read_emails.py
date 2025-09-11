import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from gmail_api import create_service

def init_gmail_service():
    """
    Initializes and returns the Gmail API service object.
    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service object.
    """
    service = create_service()
    return service

def extract_body(payload):
    """
    Recursively extracts the plain text body from a Gmail message payload.
    Ignores HTML content.
    """
    def decode_base64(data):
        return base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8', errors='ignore')

    if 'parts' in payload:
        for part in payload['parts']:
            # Recurse into nested parts
            if 'parts' in part:
                result = extract_body(part)
                if result:
                    return result
            
            # For debugging purposes
            if part.get('mimeType') == 'text/html':
                # print("Skipped HTML part")
                pass


            # Return the plain text part
            if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                return decode_base64(part['body']['data'])

    # Handle top-level body if no parts exist
    if payload.get('mimeType') == 'text/plain' and 'data' in payload.get('body', {}):
        return decode_base64(payload['body']['data'])

    return "<Empty Body>"



def get_email_details(service, user_id = 'me', label_ids = None, 
                      folder_name='Inbox', max_results=10):
    """
    Fetches a list of email message metadata from a specified Gmail folder.

    Args:
        service (googleapiclient.discovery.Resource): Authenticated Gmail API service object.
        user_id (str): Gmail user ID, usually 'me'.
        label_ids (list): List of label IDs to filter messages.
        folder_name (str): Name of the Gmail folder to fetch messages from.
        max_results (int): Maximum number of messages to fetch.

    Returns:
        list: List of message metadata dictionaries.
    """
   
    messages = []
    next_page_token = None

    if folder_name:
        label_results = service.users().labels().list(userId=user_id).execute()
        labels = label_results.get('labels', [])
        folder_label_id = next((label['id'] for label in labels if label['name'].lower() == folder_name.lower()), None)

        if folder_label_id:
            if label_ids:
                label_ids.append(folder_label_id)
            else:
                label_ids = [folder_label_id]
    
        else:
            raise ValueError(f"Folder '{folder_name}' not found.")
        
    while True:
        results = service.users().messages().list(
            userId=user_id, labelIds=label_ids,
            pageToken=next_page_token, 
            maxResults=max_results).execute()
        
        msgs = results.get('messages', [])
        messages.extend(msgs)
        next_page_token = results.get('nextPageToken')

        if not next_page_token or len(messages) >= max_results:
            break

    return messages[:max_results] if max_results else messages
    
def get_email_content(service, msg_id):
    """
    Fetches and parses the content of a Gmail message by its ID.

    Args:
        service (googleapiclient.discovery.Resource): Authenticated Gmail API service object.
        msg_id (str): The ID of the email message to fetch.

    Returns:
        dict: Dictionary containing subject, sender, recipients, body, snippet, attachments, date, starred status, and labels.
        None: If the email is promotional, spam, trash, or social.
    """
        
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = message['payload']
    headers = payload.get('headers', [])

    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "<No Subject>")
    sender = next((header['value'] for header in headers if header['name'] == 'From'), "<Unknown Sender>")
    recipients = next((header['value'] for header in headers if header['name'] =='To'), "<Unknown Recipient>")
    body = extract_body(payload)
    snippet = message.get('snippet', "<No Snippet>")
    has_attachments = any(part.get('filename') for part in payload.get('parts', []))
    date = next((header['value'] for header in headers if header['name'] =='Date'), "<Unknown Date>")
    star = message.get('labelIds') and 'STARRED' in message.get('labelIds')
    labels = message.get('labelIds', [])

    # Skip promotional, spam, trash, and social emails
    if 'CATEGORY_PROMOTIONS' in labels or 'SPAM' in labels or 'TRASH' in labels or 'CATEGORY_SOCIAL' in labels:
        # print('*' * 50)
        # print("Skipping email")
        # print('*' * 50)
        return None
    

    return {
        'subject': subject,
        'from': sender,
        'recipients': recipients,
        'body': body,
        'snippet': snippet,
        'has_attachments': has_attachments,
        'date': date,
        'starred': star,
        'labels': labels
    }

service = init_gmail_service()

email_data = get_email_details(service, folder_name='Inbox', max_results=3)


for email in email_data:
    details = get_email_content(service, email['id'])
    if details:
        print(f"Subject: {details['subject']}")
        print(f"From: {details['from']}")
        print(f"To: {details['recipients']}")
        print(f"Body: {details['body'][:100]}")  
        # print(f"Body: {details['body']}")  
        print(f"Date: {details['date']}")
        print(f"Starred: {details['starred']}")
        print(f"Labels: {details['labels']}")
        print(f"Snippet: {details['snippet']}")
        print(f"Has Attachments: {details['has_attachments']}")
        print("-" * 50)