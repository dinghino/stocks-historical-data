import os
from stonks.scraper.settings.constants import SOURCES


MOCKS_PATHS = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(MOCKS_PATHS, "options.json")
TEMP_JSON_FILE = os.path.join(MOCKS_PATHS, "temp.json")
TEMP_CSV_FILE = os.path.join(MOCKS_PATHS, "temp.csv")
EXPECTED_DIR = os.path.join(MOCKS_PATHS, 'expected')
SOURCES_DIR = os.path.join(MOCKS_PATHS, 'source')

TARGET_URLS = {}
TARGET_URLS[SOURCES.FINRA_SHORTS] = [
    "http://regsho.finra.org/CNMSshvol20210427.txt",
]
TARGET_URLS[SOURCES.SEC_FTD] = [
    "https://www.sec.gov/files/data/fails-deliver-data/cnsfails202104a.zip",
    "https://www.sec.gov/files/data/fails-deliver-data/cnsfails202104b.zip",
]

DATA_FILES = {}
DATA_FILES[SOURCES.FINRA_SHORTS] = {
    'expected': ["CNMSshvol20210427.txt"],
    'source': ["CNMSshvol20210427.txt"],
}
DATA_FILES[SOURCES.SEC_FTD] = {
    'expected': ["cnsfails202104a.txt", "cnsfails202104b.txt"],
    'source': ["cnsfails202104a.zip", "cnsfails202104b.zip"],
}

DATES = {
    "start": "",
    "end": "",
}
