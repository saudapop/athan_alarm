import os
import datetime
from fetch_prayer_times import fetch_prayer_times

YEAR = datetime.datetime.now().year

if 'data' not in os.listdir() or str(YEAR) not in os.listdir('./data'):
    fetch_prayer_times()
