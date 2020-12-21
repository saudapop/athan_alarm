import json
import datetime
import os
import requests
import argparse
from tqdm import tqdm

PARSER = argparse.ArgumentParser(
    description="Creates a folder with the entire year's prayer times in JSON format based on coordinates"
)

PARSER.add_argument('--LAT', type=float,
                    help="The geographical latitude in degrees of the location")
PARSER.add_argument('--LONG', type=float,
                    help="The geographical longitude in degrees of the location")
ARGS = PARSER.parse_args()

# Get local coordinates from https://ipapi.co/json/ or search for other coordinates at https://www.latlong.net/
if ARGS.LAT and ARGS.LONG:
    LATITUDE = ARGS.LAT
    LONGITUDE = ARGS.LONG
else:
    LOCAL_INFO = requests.get(
        'https://ipapi.co/json/').json()
    LATITUDE = LOCAL_INFO['latitude']
    LONGITUDE = LOCAL_INFO['longitude']

YEAR = datetime.datetime.year

BASE_URL = 'http://api.aladhan.com/v1/calendar?latitude={}&longitude={}&method=2&month={}&year=2020'

MONTHS = ['jan', 'feb', 'march',
          'april', 'may', 'june',
          'july', 'aug', 'sept',
          'oct', 'nov', 'dec']

TIMINGS = ["Fajr", "Dhuhr",
           "Asr", "Maghrib", "Isha", ]

BASE_PATH = './data'
PRAYER_TIMES_PATH = f'{BASE_PATH}/prayer_times'


def fetch_prayer_times():

    os.makedirs(PRAYER_TIMES_PATH, exist_ok=True)

    print(
        f'Fetching prayer times for LATITUDE={LATITUDE}, LONGITUDE={LONGITUDE}')

    for i, month in enumerate(tqdm(MONTHS, ncols=144)):
        response = requests.get(BASE_URL.format(LATITUDE, LONGITUDE, i+1))

        # create list of prayer times with just the values we are interested in
        PRAYER_TIMES = [
            {
                'date': x['date']['gregorian']['date'],
                'timings': {k: v for k, v in x['timings'].items() if k in TIMINGS}
            }
            for x in response.json()['data']
        ]
        JSON_OBJECT = json.dumps(PRAYER_TIMES, indent=4)
        FILE_NAME = f'{PRAYER_TIMES_PATH}/{i+1}_{month}.json'
        with open(FILE_NAME, "w") as FILE:
            FILE.write(JSON_OBJECT)

    # Create a template for preferences that will be used to determinte whether or not to play
    # the athan for a given prayer time
    with open(f'{BASE_PATH}/preferences.json', "w") as FILE:
        PREFERENCES = {
            "Fajr": 1,
            "Dhuhr": 1,
            "Asr": 1,
            "Maghrib": 1,
            "Isha": 1
        }
        PREFERENCES = json.dumps(PREFERENCES, indent=4)
        FILE.write(PREFERENCES)


if __name__ == '__main__':
    fetch_prayer_times()
