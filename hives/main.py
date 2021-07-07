"""Module contains common methods for the whole h1ves app."""
import os.path
import datetime


def authenticate(username, password):
    if username == 'john' and password == 'doe':
        return True
    else:
        return False


def get_time_with_millis():
    _date = datetime.datetime.now()
    formatted = _date.strftime('%a, %d.%m.%Y, %H:%M:S.%f')
    return formatted


def get_version():
    """Returns current version of application."""
    return read_file('VERSION')


def get_license():
    """Returns license text."""
    return read_file('LICENSE')


def read_file(filename):
    """Reading file from filesystem."""
    result = ''
    # Checking if file exists
    if not os.path.isfile(filename):
        # If file does not exists, return suitable information
        return "file '" + filename + "' not found"
    else:
        # If ile exists open it.
        with open(filename, 'r') as file:
            text = file.read().splitlines()

        # If file has more than 2 lines, use readlines to return pretty text.
        if len(text) > 2:
            with open(filename, 'r') as file:
                result = file.readlines()
        # If file contains just one line, return just its value.
        else:
            result = text[0]
    return result
