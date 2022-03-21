import os
import datetime

YEAR = datetime.datetime.now().year

if 'data' not in os.listdir() or str(YEAR) not in os.listdir('./data'):
	from fetch_prayer_times import fetch_prayer_times
	fetch_prayer_times()
