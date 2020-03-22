import utils
import os
from tqdm import tqdm
import argparse


def main(folder_id, folder_path_local):
    file_names_drive = get_file_names_drive(folder_id, folder_id)
    file_names_local = get_local_file_names(folder_path_local)

    files_non_uploaded = utils.get_non_uploaded_files(file_names_drive, file_names_local)
    upload_missing_photos(folder_id, folder_path_local, files_non_uploaded)

    print("The following images have been uploaded : {}".format(",".join(files_non_uploaded)))


def get_file_names_drive(folder_id, retreat):
    service = utils.get_service_drive_api()
    files = utils.get_list_files_folder(service, folder_id, page_size=1000)

    file_names = [f["name"] for f in files]

    if retreat:
        file_names = list(map(utils.retreat_image_name, file_names))

    return file_names


def get_local_file_names(folder_path):
    file_names = os.listdir(folder_path)
    return file_names


def upload_missing_photos(folder_id, folder_path, files_non_uploaded):
    for image_name in tqdm(files_non_uploaded):
        utils.upload_image(folder_id, os.path.join(folder_path, image_name))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Upload remaining (non uploaded) photos to google drive.')
    parser.add_argument('folder_id_drive', type=str,
                        help='Folder id in google drive.')
    parser.add_argument('folder_path_local', type=str,
                        help='Local folder path')
    args = parser.parse_args()
    return args.folder_id_drive, args.folder_path_local


if __name__ == '__main__':
    folder_id, folder_path_local = parse_arguments()
    main(folder_id, folder_path_local)
