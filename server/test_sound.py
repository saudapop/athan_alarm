import multiprocessing
import subprocess
import threading
import time

test_sound = '/usr/share/sounds/alsa/Front_Center.wav'
fajr = './mp3/1_regular.mp3'


def audio_jack(file_name: str):
    subprocess.Popen(['omxplayer', test_sound])


def play_athan(prayer_name):
    sound = fajr if prayer_name == 'Fajr' else 'not fajr'
    threading.Thread(target=audio_jack, args=(sound,)).start()


p = multiprocessing.Process(target=play_athan, args=('Isha',))
p.start()
time.sleep(3)
p.kill()
