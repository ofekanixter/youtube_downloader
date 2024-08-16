from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload , MediaIoBaseDownload ,  MediaInMemoryUpload
from docx import Document

import io

output_file_name= "drive_song_file.txt"

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'C:/Users/SmadarENB3/OneDrive/Desktop/ofek/programing/python/youtube_downloader/util/drive_util/youtube-downloader-service-757dd12baac1.json'
PYTHON_FOLDER_PATH='C:/Users/SmadarENB3/OneDrive/Desktop/ofek/programing/python/youtube_downloader'
class GoogleDriveClient:
    def __init__(self):
        # Authenticate with the service account
        self.credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
        self.service = build('drive', 'v3', credentials=self.credentials)

    def get_folder_id(self, folder_name, parent_folder_id=None):
        """Retrieves the ID of a folder by its name."""
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"
        
        results = self.service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
        folders = results.get('files', [])
        
        if folders:
            return folders[0].get('id')
        else:
            print(f"Folder '{folder_name}' not found.")
            return None

    def get_file_id(self, file_name, parent_folder_id=None):
        """Retrieves the ID of a file by its name."""
        query = f"name = '{file_name}'"
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"
        
        results = self.service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if files:
            return files[0].get('id')
        else:
            print(f"File '{file_name}' not found.")
            return None

    def upload_file(self, local_file_path, folder_name='songs'):
        """Uploads a file to a Google Drive folder by folder name."""
        folder_id = self.get_folder_id(folder_name)
        if not folder_id:
            print(f"Folder '{folder_name}' not found.")
            return
        name=local_file_path.split('\\')[-1]
        file_metadata = {'name': name, 'parents': [folder_id]}
        media = MediaFileUpload(local_file_path)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File uploaded successfully, file ID: {file.get("id")}')
        return file.get("id")

    def upload_mp3_file(self, local_file_path, file_name , folder_name='upload'):
        """Uploads an MP3 file to a Google Drive folder by folder name."""
        folder_id = self.get_folder_id(folder_name)
        if not folder_id:
            print(f"Folder '{folder_name}' not found.")
            return
        name=file_name
        file_metadata = {'name': name, 'parents': [folder_id]}
        media = MediaFileUpload(local_file_path, mimetype='audio/mpeg')
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'MP3 file uploaded successfully, file ID: {file.get("id")}')
        return file.get("id")
    
    def download_file(self, file_name, destination_folder=PYTHON_FOLDER_PATH , custom_name='titles.txt'):
        """Downloads a file from Google Drive by file name and optional folder name. Optionally converts .docx to .txt."""
        file_id = self.get_file_id(file_name=file_name )
        if not file_id:
            print(f"File '{file_name}' not found.")
            return

        # Download the file content
        request = self.service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        destination_txt_path = destination_folder+ '/' + custom_name
        file_content.seek(0)  # Reset buffer to start
        document = Document(file_content)
        with open(destination_txt_path, 'w', encoding='utf-8') as txt_file:
            for paragraph in document.paragraphs:
                txt_file.write(paragraph.text + '\n')

    # def download_file(self, file_name, destination_path=PYTHON_FOLDER_PATH, folder_name=None):
    #     """Downloads a file from Google Drive by file name and optional folder name."""
    #     file_id = self.get_file_id(file_name, self.get_folder_id(folder_name) if folder_name else None)
    #     if not file_id:
    #         print(f"File '{file_name}' not found.")
    #         return
        
    #     request = self.service.files().get_media(fileId=file_id)
    #     with open(destination_path, 'wb') as file:
    #         downloader = MediaIoBaseDownload(file, request)
    #         done = False
    #         while not done:
    #             status, done = downloader.next_chunk()
    #             print(f"Download {int(status.progress() * 100)}%.")

    #     print(f'File downloaded to {destination_path}')

    def edit_file(self, file_name, new_content, folder_name=None):
        """Edits the content of a file on Google Drive by file name and optional folder name."""
        file_id = self.get_file_id(file_name, self.get_folder_id(folder_name) if folder_name else None)
        if not file_id:
            print(f"File '{file_name}' not found.")
            return
        
        # Convert the new content to bytes and create an in-memory upload object
        media = MediaInMemoryUpload(new_content.encode('utf-8'), mimetype='text/plain', resumable=True)
        
        # Update the file on Google Drive
        updated_file = self.service.files().update(fileId=file_id, media_body=media).execute()
        
        print(f'File edited successfully, file ID: {updated_file.get("id")}')


    def get_file_metadata(self, file_name, folder_name=None):
        """Retrieves metadata of a file by file name and optional folder name."""
        file_id = self.get_file_id(file_name, self.get_folder_id(folder_name) if folder_name else None)
        if not file_id:
            print(f"File '{file_name}' not found.")
            return None
        
        try:
            file = self.service.files().get(fileId=file_id, fields='id, name, mimeType, modifiedTime').execute()
            return file
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
# client = GoogleDriveClient()
# # Upload a file
# # client.upload_file(r'C:\Users\SmadarENB3\OneDrive\Desktop\ofek\programing\python\titles.txt')

# # # Upload an MP3 file
# client.upload_mp3_file(r'C:\Users\SmadarENB3\OneDrive\Desktop\ofek\programing\python\Kamrad - So Good.mp3')

# # # Download a file
# # client.download_file('titles.txt', 'downloaded_file.txt', 'songs')

# # Edit a file
# # new_content = "maluma"
# # client.edit_file('titles.txt', new_content, 'songs')

# # Get file metadata
# metadata = client.get_file_metadata('titles.txt', 'songs')
# if metadata:
#     print(f"File ID: {metadata.get('id')}")
#     print(f"File Name: {metadata.get('name')}")
#     print(f"MIME Type: {metadata.get('mimeType')}")
#     print(f"Last Modified Time: {metadata.get('modifiedTime')}")