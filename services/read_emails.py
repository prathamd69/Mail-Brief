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
    Extracts the body content from the email payload.
    Args:
        payload (dict): The payload part of the email message. """
    
    body = "<Empty Body>"

    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'multipart/alternative':
                for subpart in part['parts']:
                    if subpart['mimeType'] == 'text/plain':
                        body = base64.urlsafe_b64decode(subpart['body']['data']).decode('utf-8', errors='ignore')
                        return body
            
            elif part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                return body
            
    elif body in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        return body

def get_email_details(service, user_id = 'me', label_ids = None, 
                      folder_name='Inbox', max_results= 5):
    """
    Fetches the email details using the Gmail API service and message ID.
    Args:
        service (googleapiclient.discovery.Resource): Authenticated Gmail API service object.
        msg_id (str): The ID of the email message to fetch. """
   
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
    Fetches the email content using the Gmail API service and message ID.
    Args:
        service (googleapiclient.discovery.Resource): Authenticated Gmail API service object.
        msg_id (str): The ID of the email message to fetch."""
        
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = message['payload']
    headers = payload.get('headers', [])

    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "<No Subject>")
    sender = next((header['value'] for header in headers if header['name'] == 'From'), "<Unknown Sender>")
    recipients = next((header['value'] for header in headers if header['name'] =='To'), "<Unknown Recipient>")
    snippet = message.get('snippet', "<No Snippet>")
    has_attachments = any(part.get('filename') for part in payload.get('parts', []))
    date = next((header['value'] for header in headers if header['name'] =='Date'), "<Unknown Date>")
    star = message.get('labelIds') and 'STARRED' in message.get('labelIds')
    label = ', '.join(message.get('labelIds', []))
    body = extract_body(payload)

    return {
        'subject': subject,
        'from': sender,
        'recipients': recipients,
        'snippet': snippet,
        'has_attachments': has_attachments,
        'date': date,
        'starred': star,
        'labels': label,
        'body': body
    }

service = init_gmail_service()

email_data = get_email_details(service, folder_name='Inbox', max_results=10)

for i in range(len(email_data)):
    for key,val in email_data[i].items():
        print(f"{key}: {val}")
        print()
    print("-" * 40)