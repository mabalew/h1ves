"""Logging module."""

_log = []


def log(msg):
    _log.append(msg)


def get_logs():
    return _log
