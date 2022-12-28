from . import main
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

serv = main.create_service()


def upload_file(filename, coreFile, page):
    try:
        if page == 'project':
            file_metadata = {'name': filename, 'parents': ['1z4jger2ELLj_OupQzcl8dIAAV6Q0OQki']}
        else:
            file_metadata = {'name': filename, 'parents': ['1s2TvFOuRYJnejmXPZDQE8vQ38jieqGwa']}
        media = MediaFileUpload(coreFile, mimetype='image/jpg')
        file = serv.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(F'File ID: {file.get("id")}')
        change_role_of_files(file.get("id"))
    except HttpError as error:
        print(f'An error occured: {error}')
        file = None

    return file.get("id")


def change_role_of_files(fileid):
    try:
        file_id = fileid
        request_body = {'role': 'reader', 'type': 'anyone'}
        response_permission = serv.permissions().create(
            fileId=file_id, body=request_body).execute()
    except HttpError as error:
        print(f'An error occured: {error}')

def get_file_with_id(file_id):
    try:
        res = serv.files().get(fileId=file_id, fields='webContentLink').execute()
        return res
    except HttpError as error:
        return f'An error occurred: {error}'


def delete_file(file_id):
    try:
        file = serv.files().delete(fileId=file_id).execute()
        return 'File Deleted successfully'
    except HttpError as error:
        print(f'An error occured: {error}')
        file = None
        return f'An error occurred: {error}'


def update_file(file_id):
    try:
        media = MediaFileUpload('update.png', mimetype='image/png')
        file = serv.files().update(fileId=file_id, media_body=media).execute()
        return 'File updated successfully'
    except HttpError as error:
        print(f'An error occurred: {error}')
        file = None
        return f'An error occurred: {error}'

# very import for viewing the files https://drive.google.com/uc?export=view&id=[file_id]


