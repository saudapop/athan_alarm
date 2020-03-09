# import sched
# import datetime
# import time

# my_sched = sched.scheduler(time.time, time.sleep)


# def play():
#     print('played at', datetime.datetime.now())


# foo = {
#     "date": "08-03-2020",
#     "timings": {
#         "Fajr": "16:49 (EST)",
#         "Dhuhr": "12:35 (EST)",
#         "Asr": "14:59 (EST)",
#         "Maghrib": "16:50 (EST)",
#         "Isha": "17:16 (EST)",
#     }
# }


# # returns [['HH', 'MM (EST)'], ...] a two-dimensional array of times
# parsed_timings = [v.split(':')[:2] for k, v in foo['timings'].items()]

# # remove the '(EST)' from second list item
# parsed_timings = [
#     [timing[0], timing[1].replace(' (EST)', '')]
#     for timing in parsed_timings
# ]

# time_format = '%d-%m-%Y %H:%M:%S'

# for timing in parsed_timings:

#     time_in_seconds_since_epoch = time.strptime(
#         f'{foo["date"]} {timing[0]}:{timing[1]}:00',
#         time_format
#     )

#     t = time.mktime(t)

#     EVENT_HAS_NOT_OCCURED = time.time() - t <= 1

#     if EVENT_HAS_NOT_OCCURED:
#         my_sched.enterabs(t, 1, play)
#     else:
#         pass


# my_sched.run()

import os
from pygame import mixer
import time

mixer.init()
path = './athan_mp3s'
sounds = os.listdir(path)


def play_athan(is_fajr=False):
    if is_fajr:
        i = 0
    else:
        i = 1
    mixer.music.load(f'./{path}/{sounds[i]}')
    mixer.music.play()
    time.sleep(300)


play_athan(is_fajr=True)
