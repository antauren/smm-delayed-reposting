import datetime


def is_it_publish_time(hour):
    now_time = datetime.datetime.now()

    publish_time = datetime.datetime(
        year=now_time.year,
        month=now_time.month,
        day=now_time.day,

        hour=hour
    )

    return now_time >= publish_time


def get_rus_weekday_title():
    weekdays_dict = {
        0: 'понедельник',
        1: 'вторник',
        2: 'среда',
        3: 'четверг',
        4: 'пятница',
        5: 'суббота',
        6: 'воскресенье'
    }

    weekday_num = datetime.date.today().weekday()

    return weekdays_dict[weekday_num]
