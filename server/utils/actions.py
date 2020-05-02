import json
import multiprocessing
from test import SCHEDULE, EVENTS, PREFERENCES, event_has_not_occurred


def update_preferences(NEW_PREFERENCES: dict):
    global PREFERENCES
    with open('./data/preferences.json', 'w') as FILE:
        FILE.write(json.dumps(NEW_PREFERENCES, indent=4))

    PREFERENCES = NEW_PREFERENCES


def get_current_prayers_list():
    return [event.argument[0] for event in SCHEDULE.queue]


def update_schedule():
    CURRENT_PRAYERS = get_current_prayers_list()

    for NAME_OF_PRAYER, DETAILS in EVENTS.items():
        SHOULD_SCHEDULE_EVENT = PREFERENCES[NAME_OF_PRAYER] == 1
        IS_CURRENTLY_SCHEDULED = NAME_OF_PRAYER in CURRENT_PRAYERS
        if event_has_not_occurred(DETAILS['TIME']):
            if SHOULD_SCHEDULE_EVENT and not IS_CURRENTLY_SCHEDULED:
                print(f'SCHEDULING {NAME_OF_PRAYER}')
                SCHEDULE.enterabs(*DETAILS['EVENT'])
            elif not SHOULD_SCHEDULE_EVENT and IS_CURRENTLY_SCHEDULED:
                print(f'CANCELLING {NAME_OF_PRAYER}')
                SCHEDULE.cancel(DETAILS['EVENT'])


def restart_scheduler():
    global SCHEDULING_PROGRAM
    print('RESTARTING SCHEDULING PROGRAM')
    SCHEDULING_PROGRAM.kill()
    SCHEDULING_PROGRAM.join()
    SCHEDULING_PROGRAM = multiprocessing.Process(target=SCHEDULE.run)
    SCHEDULING_PROGRAM.start()
    print('CURRENTLY SCHEDULED: ', get_current_prayers_list())

# For POST to /update-scheduler/


def refresh_scheduling_program(NEW_PREFERENCES):
    """
    Helper function that updates
    - `PREFERENCES` (JSON map of which prayers to play athan for)
    - `SCHEDULE` (adds or removes scheduled athans from `EVENTS` based on `PREFERENCES`)
    then kills the current scheduler and replaces it with a new one.
    """
    update_preferences(NEW_PREFERENCES)
    update_schedule()
    restart_scheduler()

# for GET /get-preferences/


def get_preferences():
    return {
        'data': [
            {
                'NAME': PRAYER_NAME,
                'TIME': DETAILS['TIME_PARSED'],
                'SHOULD_PLAY': PREFERENCES[PRAYER_NAME]
            } for PRAYER_NAME, DETAILS in EVENTS.items()
        ]
    }


update_schedule()
print('INIT SCHEDULE:', get_current_prayers_list())
SCHEDULING_PROGRAM = multiprocessing.Process(target=SCHEDULE.run)
SCHEDULING_PROGRAM.start()
