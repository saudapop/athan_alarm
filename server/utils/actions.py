import json
import sched
import time
import multiprocessing
from load_scheduler import EVENTS, PREFERENCES, event_has_not_occurred, logging

SCHEDULE = sched.scheduler(time.time, time.sleep)


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
        EVENT_HAS_NOT_OCCURRED = event_has_not_occurred(DETAILS['TIME'])

        if IS_CURRENTLY_SCHEDULED and not EVENT_HAS_NOT_OCCURRED:
            logging.info(
                f'CANCELLING {NAME_OF_PRAYER} BECAUSE EVENT HAS ALREADY OCCURRED')
            SCHEDULE.cancel(DETAILS['EVENT'])
        if EVENT_HAS_NOT_OCCURRED:
            if SHOULD_SCHEDULE_EVENT and not IS_CURRENTLY_SCHEDULED:
                logging.info(f'SCHEDULING {NAME_OF_PRAYER}')
                SCHEDULE.enterabs(*DETAILS['EVENT'])
            elif not SHOULD_SCHEDULE_EVENT and IS_CURRENTLY_SCHEDULED:
                logging.info(
                    f'CANCELLING {NAME_OF_PRAYER} BECAUSE NOT ON SCHEDULE')
                SCHEDULE.cancel(DETAILS['EVENT'])


def restart_scheduler():
    global SCHEDULING_PROGRAM
    logging.info('RESTARTING SCHEDULING PROGRAM')
    SCHEDULING_PROGRAM.kill()
    SCHEDULING_PROGRAM.join()
    SCHEDULING_PROGRAM = multiprocessing.Process(target=SCHEDULE.run)
    SCHEDULING_PROGRAM.start()
    logging.info(f'CURRENTLY SCHEDULED: {get_current_prayers_list()}')

# For POST to /update-scheduler/


def refresh_scheduling_program(NEW_PREFERENCES: dict):
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
logging.info(f'INIT SCHEDULE: {get_current_prayers_list()}')
SCHEDULING_PROGRAM = multiprocessing.Process(target=SCHEDULE.run)
SCHEDULING_PROGRAM.start()
