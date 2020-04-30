import os
import sys
from pushover import Pushover

def main():
    try:
        pushover = Pushover(os.environ['PUSHOVER_SNAPRAID_TOKEN'], os.environ['PUSHOVER_USER_KEY'])

        arg_str = ' '.join(sys.argv[1:])
        message = f'{os.environ["NOTIFYTYPE"]}: {arg_str}'

        pushover.send(title='UPS Event', message=message)
    except:
        pushover.send(title='UPS Notification Error!', message='Could not send notification!')
if __name__ == '__main__':
    main()
