import os
from pushover import Pushover

def main():
    try:
        pushover = Pushover(os.environ['PUSHOVER_SNAPRAID_TOKEN'], os.environ['PUSHOVER_USER_KEY'])

        message = f'Device: {os.environ["SMARTD_DEVICE"]}\n' \
                  f'Failure: {os.environ["SMARTD_FAILTYPE"]}\n' \
                  f'Error: {os.environ["SMARTD_MESSAGE"]}\n' \
                  f'First Reported: {os.environ["SMARTD_TFIRST"]}\n' \
                  f'Details: {os.environ["SMARTD_FULLMESSAGE"]}'

        pushover.send(title='SMART Status', message=message)
    except:
        pushover.send(title='SMART Notification Error!', message='Could not send notification!')
if __name__ == '__main__':
    main()
