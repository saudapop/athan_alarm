import json
import datetime
import time

TIME_FORMAT = '%d-%m-%Y %H:%M:%S'


def clean_time_string(string: str):
    return string.replace(' (EST)', '').replace(' (EDT)', '')


MONTHS = ['jan', 'feb', 'march',
          'april', 'may', 'june',
          'july', 'aug', 'sept',
          'oct', 'nov', 'dec']

PRAYER_NAMES = ["Fajr", "Dhuhr",
                "Asr", "Maghrib", "Isha", ]

FAJR = 'Fajr'

TODAY = datetime.datetime.now()
MONTH_NUM = TODAY.month
MONTH_ENG = MONTHS[MONTH_NUM - 1]
DAY = TODAY.day - 1


# read today's prayer times
with open(f'./json/{MONTH_NUM}_{MONTH_ENG}.json') as f:
    PRAYER_TIMES = json.loads(f.read())
    DATE = PRAYER_TIMES[DAY]['date']
    TIMINGS = PRAYER_TIMES[DAY]['timings']


# returns [['HH', 'MM (EST)'], ...] a two-dimensional array of times
parsed_timings = [v.split(':')[:2] for k, v in TIMINGS.items()]


# remove the '(EST)' from second list item which has the min
parsed_timings = [
    [PRAYER_NAMES[i], timing[0], clean_time_string(timing[1])]
    for i, timing in enumerate(parsed_timings)
]


for timing in parsed_timings:
    NAME_OF_PRAYER, HOUR, MIN = timing
    t = time.strptime(f'{DATE} {HOUR}:{MIN}:00', TIME_FORMAT)
    t = time.mktime(t)
    EVENT_HAS_NOT_OCCURED = time.time() - t <= 1

    if EVENT_HAS_NOT_OCCURED:
        if NAME_OF_PRAYER == FAJR:
            print('fajr time')
        else:
            print('not fajr')
    else:
        pass
