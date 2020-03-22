# google_drive_uploader
Tool in order to resume upload of a local folder to google drive (uploading only non already uploaded files).


## Before Using
* Follow the steps in the quickstart (https://developers.google.com/drive/api/v3/quickstart/python) in order to enable the Google Drive API.
* Create a file named client_id.json ({"client_id": **client_id**, "client_secret": **client_secret**})
* Go to : https://developers.google.com/oauthplayground/ and retrieve an access_token and create a file token.json (with the scopes mentionned below):
{
  "access_token": **access_token**, 
  "scope": "https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.photos.readonly https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive.scripts https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.readonly", 
  "token_type": "Bearer", 
  "expires_in": **expires_in**, 
  "refresh_token": **refresh_token**
}


## How To Use:

``python main.py drive_folder_id local_folder_path``


## Watch Out

It could have an indesirable behaviour if you have spaces in the name of files.
The algorithm retreat the names of type:
IMG_132 (2).JPG into IMG_132.JPG

## Next Steps

* Multithreading upload / Batch upload
* Include a retreat_option (to retreat file names IMG_132 (2).JPG into IMG_132.JPG)
