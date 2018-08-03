import socket
import sys

class LockError(Exception):
    def __init__(self, message):
        self.message = message

def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
        return True
    except socket.error:
        raise LockError('Lock already taken!')
