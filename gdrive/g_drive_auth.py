import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from constants import constants as c
from pathlib import Path

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']
 
auth = {
            "installed":{
                "client_id":"715887106534-3m2i759uhimd3dg1mhsl87c335oo3frp.apps.googleusercontent.com",
                "project_id":"idyll-1600381664941","auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":"L7o8D9RH9Lb_UnMl-m3KJsGd"
                ,"redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]
            }
        }

def drive_service():
    'authentification'

    credentials = None
    tkn = c.DIR_NAME / 'token.pickle'
    if os.path.exists(tkn):
        with open(tkn, 'rb') as token:
            credentials = pickle.load(token)
            print('\ncredentials succesfully read\n')
    # if nothing available
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # authenticate using id
            try:
                # flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
                flow = InstalledAppFlow.from_client_config(auth, SCOPES)
            except ValueError:
                print(c.RED + 'client id has changed or been tampered with' + c.END)
                raise
            credentials = flow.run_local_server(port=0)
        with open(tkn, 'wb') as token:
            # save creds
            pickle.dump(credentials, token)
            print('\ncredentials created\n')
    return build('drive', 'v3', credentials=credentials)


def upload():
    'uploads to gdrive'

    service = drive_service()
    p_folder_metadata = {
        'name': 'idyll_backups',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    p_file = service.files().create(body=p_folder_metadata, fields='id').execute()
    p_folder_id = p_file.get('id')
    print('parent folder created as \'idyll_backups\': ' + p_folder_id + '\n')
    # list of all subdirectories
    folders = [f for f in os.listdir(c.DIR_NAME) if os.path.isdir(c.DIR_NAME / f)]
    for f in folders:
        folder_metadata = {
            "name": f,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [p_folder_id]
        }
        file = service.files().create(body=folder_metadata, fields='id').execute()
        s_folder_id = file.get('id')
        print(str(f) + ' folder created: ' + str(s_folder_id))

        # subfiles in subfolders
        files = [c for c in os.listdir(c.DIR_NAME / f) if c.endswith('.txt')]
        for subfile in files:
            file_metadata = {
                'name': str(subfile),
                'parents': [s_folder_id]
            }
            media = MediaFileUpload(str(c.DIR_NAME / f / subfile),
                    resumable=True)
            file = service.files().create(body=file_metadata,
                                          media_body = media,
                                          fields='id').execute()
            print('file created: ' + str(subfile) + ': ' + file.get('id'))
    print(c.YELLOW + '\nbackup successful\n' + c.END)
