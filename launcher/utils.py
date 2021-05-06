import os
from pathlib import Path

ROOT = os.path.dirname(os.path.abspath(__file__))


def parse_path(path):
    if path.startswith('~'):
        path = path.replace('~', Path.home())
    elif path.startswith('.'):
        path = ''.join([os.getcwd(), *path[1:]])
    return path
