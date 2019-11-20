def search_files_by_name(name: str, drive_service) -> list:
    query = "name='{}'".format(name)
    return search_files(query, drive_service)


def search_files(query: str, drive_service) -> list:
    '''https://developers.google.com/drive/api/v3/search-files'''

    files = []

    page_token = None
    while True:
        response = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()

        for file in response.get('files', []):
            files.append(file)

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    return files
