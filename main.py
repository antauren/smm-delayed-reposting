import os.path
from googleapiclient.discovery import build

import time

from dotenv import dotenv_values

from social_media.facebook import post_facebook
from social_media.telegram import post_telegram
from social_media.vkontakte import post_vkontakte

# The ID and range of a sample spreadsheet.

from utils.datetime import is_it_publish_time, get_rus_weekday_title
from utils.google_auth import get_credentials
from utils.google_spreadsheet import get_google_drive_id, get_spreadsheet_id_by_title, get_values_from_spreadsheet, \
    update_values_in_spreadsheet
from utils.pydrive import get_file_list, get_drive, download_txt_file_from_google_drive, \
    download_img_file_from_google_drive


def sleep(minutes):
    time.sleep(minutes * 60)


def is_yes(word: str) -> bool:
    word = word.strip().lower()

    return word == 'да' or word == 'yes'


def check_spreadsheet(dotenv_dict, spreadsheet_id, range, drive):
    day = get_rus_weekday_title()

    img_dir = 'images'
    os.makedirs(img_dir, exist_ok=True)

    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    service_spreadsheets_values = service.spreadsheets().values()

    values = get_values_from_spreadsheet(service_spreadsheets_values, spreadsheet_id, range)

    for num, row in enumerate(values[1:]):
        sheet_row_num = num + 1

        vk_index, telegram_index, facebook_index = 0, 1, 2
        publish_day, publish_hour = row[3], row[4]
        doc_hyperlink, img_hyperlink = row[5], row[6]
        is_posted_index = 7

        if is_yes(row[is_posted_index]):
            continue

        if day != publish_day:
            continue

        if not is_it_publish_time(publish_hour):
            continue

        img_path = ''
        if img_hyperlink.strip():
            file_id = get_google_drive_id(img_hyperlink)
            img_path = download_img_file_from_google_drive(file_id, drive, img_dir)

        text = ''
        if doc_hyperlink.strip():
            file_id = get_google_drive_id(doc_hyperlink)
            text = download_txt_file_from_google_drive(file_id, drive)

        text = text.strip()
        if not os.path.exists(img_path):
            img_path = None

        if (img_path is None) and not text:
            continue

        sleep(0.5)

        is_all_posted = True

        if is_yes(row[vk_index]):
            try:
                post_vkontakte(img_path, dotenv_dict['VKONTAKTE_TOKEN'], dotenv_dict['VKONTAKTE_GROUP_ID'], text)
                values[sheet_row_num][vk_index] = 'нет'
            except:
                is_all_posted = False

        if is_yes(row[telegram_index]):
            try:
                post_telegram(img_path, dotenv_dict['TELEGRAM_TOKEN'], dotenv_dict['TELEGRAM_CHAT_ID'], text)
                values[sheet_row_num][telegram_index] = 'нет'
            except:
                is_all_posted = False

        if is_yes(row[facebook_index]):
            try:
                post_facebook(img_path, dotenv_dict['FACEBOOK_TOKEN'], dotenv_dict['FACEBOOK_GROUP_ID'], text)
                values[sheet_row_num][facebook_index] = 'нет'

            except:
                is_all_posted = False

        if is_all_posted:
            values[sheet_row_num][is_posted_index] = 'да'

        update_values_in_spreadsheet(service_spreadsheets_values, spreadsheet_id, values, range)


if __name__ == '__main__':

    drive = get_drive()
    file_list = get_file_list(drive)

    dotenv_dict = dotenv_values()

    spreadsheet_id = get_spreadsheet_id_by_title(dotenv_dict['TITLE'], file_list)

    while True:
        check_spreadsheet(dotenv_dict, spreadsheet_id, dotenv_dict['RANGE'], drive)
        sleep(5)
