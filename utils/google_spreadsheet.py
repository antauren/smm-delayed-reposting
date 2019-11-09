from urllib.parse import urlparse

from .extracturl import extract


def get_values_from_spreadsheet(service_spreadsheets_values, spreadsheet_id, range):
    '''https://developers.google.com/sheets/api/quickstart/python'''

    result = service_spreadsheets_values.get(
        spreadsheetId=spreadsheet_id,
        range=range,
        valueRenderOption='FORMULA'
    ).execute()

    values = result.get('values', [])

    return values


def update_values_in_spreadsheet(service_spreadsheets_values, spreadsheet_id, values, range):
    '''https://developers.google.com/sheets/api/guides/values#writing_to_a_single_range'''

    service_spreadsheets_values.update(
        spreadsheetId=spreadsheet_id,
        range=range,
        valueInputOption='USER_ENTERED',
        body={'values': values}
    ).execute()


def get_google_drive_id(text: str) -> str:
    url_list = extract(text)
    url = url_list[0]

    query = urlparse(url).query
    id_ = query.split('=')[1].split('"')[0]

    return id_


def get_spreadsheet_id_by_title(title, file_list):
    for file_ in file_list:
        if file_['title'] == title:
            return file_['id']
