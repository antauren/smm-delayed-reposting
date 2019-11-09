import datetime
import time


def is_it_publish_time(hour):
    now_time = datetime.datetime.now()

    publish_time = datetime.datetime(
        year=now_time.year,
        month=now_time.month,
        day=now_time.day,

        hour=hour
    )

    return now_time >= publish_time


def time_sleep(minutes):
    time.sleep(minutes * 60)
