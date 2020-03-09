import json
import os
import requests

# Get coordiantes from https://www.latlong.net/

LATITUDE =  # fill in your latitude
LONGITUDE =  # Fill in your longitude

BASE_URL = 'http://api.aladhan.com/v1/calendar?latitude={}&longitude={}&method=2&month={}&year=2020'


MONTHS = ['jan', 'feb', 'march',
          'april', 'may', 'june',
          'july', 'aug', 'sept',
          'oct', 'nov', 'dec']

TIMINGS = ["Fajr", "Dhuhr",
           "Asr", "Maghrib", "Isha", ]

for i, month in enumerate(MONTHS):
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
    with open('./json/{}_{}.json'.format(i+1, month), "w") as FILE:
        FILE.write(JSON_OBJECT)
