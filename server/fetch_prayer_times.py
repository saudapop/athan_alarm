import json
import os
import requests
import argparse
from tqdm import tqdm

PARSER = argparse.ArgumentParser(
    description="Creates a folder with the entire year's prayer times in JSON format based on longitude"
)

PARSER.add_argument('--LAT', type=float, required=True,
                    help="The physical latitude in degrees of the location")
PARSER.add_argument('--LONG', type=float, required=True,
                    help="The physical longitude in degrees of the location")

ARGS = PARSER.parse_args()


# Get coordinates from https://www.latlong.net/

LATITUDE = ARGS.LAT
LONGITUDE = ARGS.LONG

BASE_URL = 'http://api.aladhan.com/v1/calendar?latitude={}&longitude={}&method=2&month={}&year=2020'

MONTHS = ['jan', 'feb', 'march',
          'april', 'may', 'june',
          'july', 'aug', 'sept',
          'oct', 'nov', 'dec']

TIMINGS = ["Fajr", "Dhuhr",
           "Asr", "Maghrib", "Isha", ]

FOLDER = 'prayer_times'

if FOLDER not in os.listdir():
    os.mkdir(f'./{FOLDER}')

print(
    f'Fetching prayer times for LATITUDE={ARGS.LAT}, LONGITUDE={ARGS.LONG}')

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
    FILE_NAME = f'./{FOLDER}/{i+1}_{month}.json'
    with open(FILE_NAME, "w") as FILE:
        FILE.write(JSON_OBJECT)

with open('./preferences.json', "w") as FILE:
    PREFERENCES = {
        "Fajr": 1,
        "Dhuhr": 1,
        "Asr": 1,
        "Maghrib": 1,
        "Isha": 1
    }
    PREFERENCES = json.dumps(PREFERENCES, indent=4)
    FILE.write(PREFERENCES)
