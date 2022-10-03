import os

from pushover import Pushover

def check_updates(application, pushover):
    application = application.strip()

    os.chdir(f"{os.environ['AUR_DIR']}/{application}")

    subprocess.run(['git', 'fetch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    local_result = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    upstream_result = subprocess.run(['git', 'rev-parse', '@{u}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if local_result.stdout.decode('UTF-8') == upstream_result.stdout.decode('UTF-8'):
        pushover.send(title='Update Available!', message=f'{application} can be updated!')
        return True

    return False

def main():
    pushover = Pushover(os.environ['PUSHOVER_AUR_TOKEN'], os.environ['PUSHOVER_USER_KEY'])

    for application in os.environ['AUR_APPLICATIONS'].split(','):
        check_updates(application, pushover)

if __name__ == '__main__':
    main()
