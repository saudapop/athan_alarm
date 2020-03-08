import json
import datetime
import time
import sched

from pygame import mixer


def clean_time_string(string: str):
    return string.replace(' (EST)', '').replace(' (EDT)', '')


################### SOUND SETUP ###########################
mixer.init()
mixer.music.load('./athan_mp3s/1_alafasy.mp3')
mixer.music.set_volume(1.0)


def play_athan():
    mixer.music.play()
#---------------------------------------------------------#

################### DATE CONSTANTS ########################


MONTHS = ['jan', 'feb', 'march',
          'april', 'may', 'june',
          'july', 'aug', 'sept',
          'oct', 'nov', 'dec']

TODAY = datetime.datetime.now()
MONTH_NUM = TODAY.month
MONTH_ENG = MONTHS[MONTH_NUM - 1]
DAY = TODAY.day - 1
#---------------------------------------------------------#


# read today's prayer times
with open(f'./json/{MONTH_NUM}_{MONTH_ENG}.json') as f:
    PRAYER_TIMES = json.loads(f.read())
    DATE = PRAYER_TIMES[DAY]['date']
    TIMINGS = PRAYER_TIMES[DAY]['timings']


# returns [['HH', 'MM (EST)'], ...] a two-dimensional array of times
parsed_timings = [v.split(':')[:2] for k, v in TIMINGS.items()]


# remove the '(EST)' from second list item which has the min
parsed_timings = [
    [timing[0], clean_time_string(timing[1])]
    for timing in parsed_timings
]


time_format = '%d-%m-%Y %H:%M:%S'

for timing in parsed_timings:
	HOUR, MIN = timing
    t = time.strptime(f'{DATE} {HOUR}:{MIN}:00',time_format)
    t = time.mktime(t)

    EVENT_HAS_NOT_OCCURED = time.time() - t <= 1

    if EVENT_HAS_NOT_OCCURED:
        my_sched.enterabs(t, 1, play_athan)
    else:
        pass


my_sched.run()
