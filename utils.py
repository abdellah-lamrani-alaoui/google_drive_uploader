from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
import oauth2client
import datetime
import json
import os


CRENDATIALS_FILE = "client_id.json"
TOKEN_FILE = "token.json"


def get_list_files_folder(service, folder_id, page_size=1000):
    results = service.files().list(q="'{}' in parents".format(folder_id), pageSize=page_size).execute()
    files = results.get('files', [])
    next_page_token = results.get("nextPageToken", None)

    while next_page_token:
        results = service.files().list(q="'{}' in parents".format(folder_id),
                                       pageSize=page_size,
                                       pageToken=next_page_token).execute()
        next_page_token = results.get("nextPageToken", None)
        files += results.get('files', [])

    return files


def retreat_image_name(name):
    name_parts = name.split(" ")
    if len(name_parts) == 1:
        return name_parts[0]

    extension = name_parts[-1].split(".")[-1]
    retreated_name = name_parts[0] + "." + extension

    return retreated_name


def get_non_uploaded_files(files_drive, files_local):
    return [file_name for file_name in files_local if file_name not in set(files_drive)]


def upload_image(folder_id, image_path):
    image_name = os.path.basename(image_path)
    file_metadata = {'name': image_name, 'parents': [folder_id]}
    media = MediaFileUpload(image_path,
                            mimetype='image/jpeg')
    service = get_service_drive_api()
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()


service = None
def get_service_drive_api():
    global service
    if service is not None:
        return service
    credentials = get_credentials_from_token()
    service = discovery.build('drive', 'v3', http=credentials.authorize(Http()))
    return service


def get_client_id_secret():
    with open(CRENDATIALS_FILE, "r") as f:
        data_secret = json.load(f)
    return data_secret["client_id"], data_secret["client_secret"]


def get_credentials_from_token():
    with open(TOKEN_FILE, "r") as f:
        token = json.load(f)

    client_id, client_secret = get_client_id_secret()

    access_token = token["access_token"]

    if "refresh_token" not in token:
        refresh_token = None
    else:
        refresh_token = token["refresh_token"]
    expires_in = datetime.datetime.fromtimestamp(token["expires_in"])
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
    credentials = oauth2client.client.GoogleCredentials(
        access_token, client_id, client_secret,
        refresh_token, expires_in,
        "https://accounts.google.com/o/oauth2/token",
        user_agent)

    return credentials



########################### Application credentials ###################################

SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
CREDENTIALS_STORAGE_FILE = "creds.json"


def get_credentials():
    store = oauth2client.file.Storage(CREDENTIALS_STORAGE_FILE)
    creds = store.get()

    if not creds or creds.invalid:
        flow = oauth2client.client.flow_from_clientsecrets(CRENDATIALS_FILE, SCOPES)
        creds = oauth2client.tools.run_flow(flow, store)

    return creds


service = None
def get_drive_service(creds=None):
    global service
    if service is not None:
        return service

    if creds is None:
        creds = get_credentials()
    service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    return service
