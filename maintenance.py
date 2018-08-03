import os

from pushover import Pushover
from snapraid import Snapraid, SnapraidError
from lock import get_lock, LockError

MAX_FILES_REMOVED = 50
SCRUB_FREQUENCY_DAYS = 7
SCRUB_ARRAY_PERCENTAGE = 25

def obtain_lock(pushover):
    try:
        return get_lock('maintenance')
    except LockError as err:
        message = 'Error when attempting to obtain an exclusive lock in ' \
                  'order to run maintenance. Message:\n' \
                  f'{err.message}'
        pushover.send(title='Error!', message=message)
        return False

def execute_snapraid_scrub(pushover):
    status = Snapraid.status()

    if status.newest_scrubbed_at >= SCRUB_FREQUENCY_DAYS:
        message = f'Last scrub was {status.newest_scrubbed_at} days ago. ' \
                  f'Set to scrub {SCRUB_ARRAY_PERCENTAGE}% of the array ' \
                  f'every {SCRUB_FREQUENCY_DAYS} days.'
        pushover.send(title='Scrubbing...', message=message)

        scrub = Snapraid.scrub(percentage=SCRUB_ARRAY_PERCENTAGE)
        pushover.send(title='Scrub Complete!', message=scrub.result)

        pushover.send(title='Array Status', message=Snapraid.status().summary)
    else:
        pushover.send(title='Array Status', message=status.summary)

    return True

def execute_snapraid_maintenance(pushover):
    try:
        diff = Snapraid.diff()

        if not diff.has_changes():
            pushover.send(title='Sync Status', message='No changes detected! Skipping sync.')
            return execute_snapraid_scrub(pushover)

        if diff.removed > MAX_FILES_REMOVED:
            message = f'{diff.removed} files have been removed, which exceeds the threshold ' \
                      f'of {MAX_FILES_REMOVED}. Sync has been aborted.'
            pushover.send(title='Sync Failure!', message=message)
            return False

        pushover.send(title='Sync Beginning...', message=diff.text)

        output = Snapraid.sync()
        pushover.send(title='Sync Complete!', message=output)

        return execute_snapraid_scrub(pushover)
    except SnapraidError as err:
        message = 'An error occurred during sync!\n' \
                  f'Error code {err.error_code} was returned:\n' \
                  f'{err.message}'
        pushover.send(title='Error!', message=message)
        return False

def main():
    pushover = Pushover(os.environ['PUSHOVER_SNAPRAID_TOKEN'], os.environ['PUSHOVER_USER_KEY'])

    if not obtain_lock(pushover):
        return False

    return execute_snapraid_maintenance(pushover)

if __name__ == '__main__':
    main()
