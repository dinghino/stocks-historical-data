import os
from stonks.components.handlers.finra import source as finra_source
from stonks.components.handlers.secftd import source as secftd_source


MOCKS_PATHS = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(MOCKS_PATHS, "options.json")
EMPTY_SETTINGS_PATH = os.path.join(MOCKS_PATHS, "options_empty.json")
WRONG_SETTINGS_PATH = os.path.join(MOCKS_PATHS, "options_wrong.json")
TEMP_JSON_FILE = os.path.join(MOCKS_PATHS, "temp.json")
TEMP_CSV_FILE = os.path.join(MOCKS_PATHS, "temp.csv")
EXPECTED_DIR = os.path.join(MOCKS_PATHS, 'expected')
SOURCES_DIR = os.path.join(MOCKS_PATHS, 'source')

TARGET_URLS = {}
TARGET_URLS[finra_source] = [
    "http://regsho.finra.org/CNMSshvol20210427.txt",
]
TARGET_URLS[secftd_source] = [
    "https://www.sec.gov/files/data/fails-deliver-data/cnsfails202104a.zip",
    "https://www.sec.gov/files/data/fails-deliver-data/cnsfails202104b.zip",
]

DATA_FILES = {}
DATA_FILES[finra_source] = {
    'expected': ["CNMSshvol20210427.txt"],
    'source': ["CNMSshvol20210427.txt"],
}
DATA_FILES[secftd_source] = {
    'expected': ["cnsfails202104a.txt", "cnsfails202104b.txt"],
    'source': ["cnsfails202104a.zip", "cnsfails202104b.zip"],
}

DATES = {
    "start": "",
    "end": "",
}
