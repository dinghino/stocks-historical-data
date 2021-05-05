import os
from pathlib import Path

# Stonks package root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# points to the repository root
PROJECT_ROOT = Path(ROOT_DIR).parent

# Directory where the app will store by default its settings, keys and such
DEFAULT_DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
# The path for the default settings object if nothing else is provided.
# This is supposed to be 'protected' inside the install path
DEFAULT_SETTINGS_PATH = os.path.join(DEFAULT_DATA_DIR, 'options.json')
# TODO: This won't work at release, we better find a new way to set a
# default. $HOME/stocks/output/, maybe? should test on *nix/windows
# environment though.
DEFAULT_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'output')
