import json
import datetime
import time
import sched
import os
from pygame import mixer

SCHEDULE = sched.scheduler(time.time, time.sleep)


def clean_time_string(string: str):
    return string.replace(' (EST)', '').replace(' (EDT)', '')


################### SOUND SETUP ###########################
mixer.init()
path = './athan_mp3s'
sounds = os.listdir(path)


def play_athan(is_fajr=False):
    i = 0 if is_fajr else 1
    mixer.music.load(f'./{path}/{sounds[i]}')
    mixer.music.play()
    time.sleep(300)


def play_fajr_athan():
    play_athan(is_fajr=True)
#---------------------------------------------------------#


######################## CONSTANTS ########################
PRAYER_NAMES = ["Fajr", "Dhuhr",
                "Asr", "Maghrib", "Isha", ]

FAJR = 'Fajr'

MONTHS = ['jan', 'feb', 'march',
          'april', 'may', 'june',
          'july', 'aug', 'sept',
          'oct', 'nov', 'dec']

TODAY = datetime.datetime.now()
MONTH_NUM = TODAY.month
MONTH_ENG = MONTHS[MONTH_NUM - 1]
DAY = TODAY.day - 1

TIME_FORMAT = '%d-%m-%Y %H:%M:%S'
#---------------------------------------------------------#


# read today's prayer times
with open(f'./json/{MONTH_NUM}_{MONTH_ENG}.json') as f:
    PRAYER_TIMES = json.loads(f.read())
    DATE = PRAYER_TIMES[DAY]['date']
    TIMINGS = PRAYER_TIMES[DAY]['timings']


# returns [['HH', 'MM (EST)'], ...] a two-dimensional array of times for today
PARSED_TIMINGS = [v.split(':')[:2] for k, v in TIMINGS.items()]


# remove the '(EST)' from second list item which is a string containing the minutes
PARSED_TIMINGS = [
    [PRAYER_NAMES[i], timing[0], clean_time_string(timing[1])]
    for i, timing in enumerate(PARSED_TIMINGS)
]


for PRAYER in PARSED_TIMINGS:
    NAME_OF_PRAYER, HOUR, MIN = PRAYER
    t = time.strptime(f'{DATE} {HOUR}:{MIN}:00', TIME_FORMAT)
    t = time.mktime(t)
    EVENT_HAS_NOT_OCCURED = time.time() - t <= 1
    if EVENT_HAS_NOT_OCCURED:
        if NAME_OF_PRAYER == FAJR:
            SCHEDULE.enterabs(t, 1, play_fajr_athan)
        else:
            SCHEDULE.enterabs(t, 1, play_athan)
    else:
        pass


SCHEDULE.run()
