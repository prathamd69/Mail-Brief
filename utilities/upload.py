from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from services.read_emails import init_gmail_service, get_email_details, get_email_content
from config import DRIVE_FOLDER_ID

def upload_to_drive(drive_service, file_path, folder_id=None):
    """
    Uploads a file to Google Drive.

    Args:
        drive_service (googleapiclient.discovery.Resource): Authenticated Google Drive API service object.
        file_path (str): Path to the file to be uploaded.
        folder_id (str, optional): ID of the Drive folder to upload the file into. If None, uploads to root.

    Returns:
        str: The file ID of the uploaded file.

    This function creates file metadata, attaches the file, and uploads it to Google Drive.
    If a folder ID is provided, the file is uploaded to that folder.
    """
    file_metadata = {'name': 'emails.json'}
    if folder_id:
        file_metadata['parents'] = [folder_id]  

    media = MediaFileUpload(file_path, mimetype='application/json')
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"✅ Uploaded emails.json to Drive")
    return uploaded_file['id']


