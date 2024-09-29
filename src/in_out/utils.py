import time
from functools import wraps


def retry_on_os_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        count = 2
        while count >= 0:
            try:
                return func(*args, **kwargs)
            except OSError:
                time.sleep(0.05)

    return wrapper
