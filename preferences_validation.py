from test import PRAYER_NAMES
from flask import jsonify


class UpdatePreferencesException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def validate_preferences_payload(NEW_PREFERENCES):
    CORRECT_PAYLOAD_EXAMPLE = {
        'correct_payload': f'Should look similar to this: {{ "Fajr": 0, "Dhuhr": 0, "Asr": 0, "Maghrib": 1, "Isha": 1}}'
    }
    if NEW_PREFERENCES is None:
        raise UpdatePreferencesException(
            'Payload is missing from the request body. See preferences.json for an example of what it should look like',
            payload=CORRECT_PAYLOAD_EXAMPLE
        )

    for k, v in NEW_PREFERENCES.items():
        if k not in PRAYER_NAMES:
            raise UpdatePreferencesException(
                f'{k} should not exist in the payload or is mispelled or something else...',
                payload=CORRECT_PAYLOAD_EXAMPLE
            )
    for NAME in PRAYER_NAMES:
        try:
            NEW_PREFERENCES[NAME]
        except:
            raise UpdatePreferencesException(
                f'{NAME} is missing from the payload.', payload=CORRECT_PAYLOAD_EXAMPLE
            )
        if type(NEW_PREFERENCES[NAME]) is not int:
            raise UpdatePreferencesException(
                f'The value for {NAME} must be an integer.', payload=CORRECT_PAYLOAD_EXAMPLE
            )
        if int(NEW_PREFERENCES[NAME]) < 0 or int(NEW_PREFERENCES[NAME]) > 1:
            print(f'{int(NEW_PREFERENCES[NAME])}')
            raise UpdatePreferencesException(
                f'{NAME} must have a value of either 0 or 1', payload=CORRECT_PAYLOAD_EXAMPLE
            )
