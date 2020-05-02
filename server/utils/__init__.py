import os
from fetch_prayer_times import fetch_prayer_times

if 'data' not in os.listdir() or 'prayer_times' and 'preferences.json' not in os.listdir('./data'):
    fetch_prayer_times()
