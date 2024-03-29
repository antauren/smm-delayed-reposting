import os.path

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.

    drive = GoogleDrive(gauth)  # Create GoogleDrive instance with authenticated GoogleAuth instance

    # Auto-iterate through all files in the root folder.

    return drive


def download_txt_file_from_google_drive(id, drive):
    file_ = drive.CreateFile({'id': id})

    return file_.GetContentString(mimetype='text/plain')


def download_img_file_from_google_drive(id, drive, dir_path, suffix=''):
    file_ = drive.CreateFile({'id': id})

    file_.FetchMetadata()
    filename = file_['originalFilename']

    if suffix:
        root, ext = os.path.splitext(filename)
        filename = '{}_{}{}'.format(root, suffix, ext)

    filepath = os.path.join(dir_path, filename)

    file_.GetContentFile(filepath)

    return filepath
