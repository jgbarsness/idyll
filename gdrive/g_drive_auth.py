import pickle
from os import path, listdir
from constants import constants as c
from pathlib import Path
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']
 
AUTH = {
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

    # google API imports expensive - wrap in function to eliminate unnecessary startup
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow

    credentials = None
    tkn = c.DIR_NAME / 'token.pickle'
    if path.exists(tkn):
        with open(tkn, 'rb') as token:
            credentials = pickle.load(token)
            print('\ncredentials successfully read\n')
    # if nothing available
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            print('credentials refreshed')
        else:
            # authenticate using id
            try:
                # use hardcoded id/secret
                flow = InstalledAppFlow.from_client_config(AUTH, SCOPES)
            except ValueError:
                print(c.RED + 'client id has changed or been tampered with' + c.END)
                raise
            credentials = flow.run_local_server(port=0)
        with open(tkn, 'wb') as token:
            # save creds
            pickle.dump(credentials, token)
            print('\nnew or refreshed credentials saved in: ' + c.PURPLE + str(tkn) + c.END + '\n')
    return build('drive', 'v3', credentials=credentials)


def upload():
    'uploads to gdrive'

    from google.auth.transport.requests import Request
    from googleapiclient.http import MediaFileUpload

    service = drive_service()

    # search for instance of backup folder
    is_instance = False
    instance_id = None
    found = service.files().list(q="name='idyll_backups'" and "mimeType = 'application/vnd.google-apps.folder'" and "trashed = false",
                                 spaces='drive',
                                 fields='files(id, name)'
                                 ).execute()
    for file in found.get('files', []):
        if file.get('name') == 'idyll_backups':
            is_instance = True
            instance_id = file.get('id')
            print('found existing backup: ' + instance_id + '\n')

    if not is_instance:
        p_folder_metadata = {
            'name': 'idyll_backups',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        p_file = service.files().create(body=p_folder_metadata, fields='id').execute()
        instance_id = p_file.get('id')
        print('parent folder created as \'idyll_backups\': ' + instance_id + '\n')

    date_folder_meta = {
        'name': str(datetime.now()),
        'mimeType': 'application/vnd.google-apps.folder',
        "parents": [instance_id]
    }
    date_folder = service.files().create(body=date_folder_meta, fields='id').execute()
    date_folder_id = date_folder.get('id')
    print('sub folder created as: ' + date_folder_id + '\n')
    # list of all subdirectories
    folders = [f for f in listdir(c.DIR_NAME) if path.isdir(c.DIR_NAME / f)]
    for f in folders:
        folder_metadata = {
            "name": f,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [date_folder_id]
        }
        file = service.files().create(body=folder_metadata, fields='id').execute()
        s_folder_id = file.get('id')
        print(str(f) + ' folder created: ' + str(s_folder_id))

        # subfiles in subfolders
        files = [c for c in listdir(c.DIR_NAME / f) if c.endswith('.txt')]
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
            print(str(subfile) + ' uploaded: ' + file.get('id'))
        # new line inbetween folders
        print()
    print(c.YELLOW + 'backup successful\n' + c.END)
