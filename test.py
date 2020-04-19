import json
import datetime
import time
import sched
import os
import logging
import threading
import subprocess

# logging.basicConfig(
#     filename="/home/pi/Desktop/azan_prayer_times/athan.log",
#     level=logging.INFO,
#     format="%(asctime)s:%(message)s",
# )

SCHEDULE = sched.scheduler(time.time, time.sleep)


def clean_time_string(string: str):
    return string.replace(' (EST)', '').replace(' (EDT)', '')


################### SOUND SETUP ###########################
fajr = '0_alafasy.wav'
regular = '1_mecca.wav'


def bluetooth_speaker(file_name: str):
    print('bluetooth speaker')
    # subprocess.Popen(['aplay',
    #                   '-D',
    #                   'bluealsa:SRV=org.bluealsa,DEV=EB:79:35:3C:D6:F3,PROFILE=a2dp',
    #                   f'/home/pi/Desktop/azan_prayer_times/wav/{file_name}'])


def audio_jack(file_name: str):
    print('audio jack')
    # time.sleep(.1)
    # subprocess.Popen(['aplay',
    #                   f'/home/pi/Desktop/azan_prayer_times/wav/{file_name}'])


def play_athan(prayer_name):
    # logging.info(f'playing {prayer_name} athan')
    sound = fajr if prayer_name == 'Fajr' else regular
    threading.Thread(target=bluetooth_speaker, args=(sound,)).start()
    threading.Thread(target=audio_jack, args=(sound,)).start()


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
EVENTS = []
#---------------------------------------------------------#


# read today's prayer times
with open(f'./json/{MONTH_NUM}_{MONTH_ENG}.json') as f:
    PRAYER_TIMES = json.loads(f.read())
    DATE = PRAYER_TIMES[DAY]['date']
    TIMINGS = PRAYER_TIMES[DAY]['timings']

logging.info(f'\ntimings fetched for {DATE}\n')
# returns [['HH', 'MM (EST)'], ...] a two-dimensional array of times for today
PARSED_TIMINGS = [v.split(':')[:2] for k, v in TIMINGS.items()]


# remove the '(EST)' from second list item which is a string containing the minutes
PARSED_TIMINGS = [
    [PRAYER_NAMES[i], timing[0], clean_time_string(timing[1])]
    for i, timing in enumerate(PARSED_TIMINGS)
]

# loop over timings and schedule them if they haven't occured
for PRAYER in PARSED_TIMINGS:
    NAME_OF_PRAYER, HOUR, MIN = PRAYER
    t = time.strptime(f'{DATE} {HOUR}:{MIN}:00', TIME_FORMAT)
    t = time.mktime(t)
    EVENT_HAS_NOT_OCCURED = time.time() - t <= 1
    if EVENT_HAS_NOT_OCCURED:
        NEW_EVENT = SCHEDULE.enterabs(
            t, 1, play_athan, argument=(NAME_OF_PRAYER,))
        EVENTS.append([PRAYER, NEW_EVENT])
    else:
        pass

try:
    # print(*EVENTS, sep='\n')
    SCHEDULE.cancel(EVENTS[1][1])
    print(SCHEDULE.queue)
    # print(*EVENTS, sep='\n')
    # SCHEDULE.enter(*EVENTS[0][1])
    SCHEDULE.run()
except Exception as e:
    print(e)
    # logging.info(f'error {e}')
