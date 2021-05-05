import os
from pathlib import Path


def path_contains_filename(path):
    """ Check for valid data output filename using the extension."""
    # TODO: (Proposition) Refactor into writer/filename(s) class in order
    # to allow different writers to define own extension to check, if any.
    extensions = ['.csv', '.txt']
    for ext in extensions:
        if path.endswith(ext):
            return True
    return False


def parse_home_path(path):
    """if path starts with ~ consider it the usual $HOME shortcut and
    # replace it with that path"""
    if path.startswith("~"):  # pragma: no cover
        path = path.replace('~', str(Path.home()))
    return path


def parse_pwd_path(path):
    """Replace the initial '.' in a path with the current working dir"""
    if path.startswith('.'):
        path = ''.join([os.getcwd(), *path[1:]])
    return path
