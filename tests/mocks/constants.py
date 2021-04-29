import os
from scraper.settings.constants import SOURCES


MOCK_PATHS    = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(MOCK_PATHS, "options.json")
TEMP_TO_FILE  = os.path.join(MOCK_PATHS, "temp.json")

EXPECTED_DIR  = os.path.join(MOCK_PATHS, 'expected')
SOURCES_DIR   = os.path.join(MOCK_PATHS, 'source')

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
    'source' : ["CNMSshvol20210427.txt"],
}
DATA_FILES[SOURCES.SEC_FTD] = {
    'expected': ["cnsfails202104a.txt","cnsfails202104b.txt"],
    'source': ["cnsfails202104a.zip","cnsfails202104b.zip"],
}


DATES = {
    "start": "",
    "end": "",
}





# class FakeDataItem:
#     def __init__(self, expected, source_fname, source_addr_base):
#         self.expected_fname = expected
#         self.source_fname = source_fname
#         self.source_addr= source_addr_base + source_fname


# finra_shorts_1 = FakeDataItem(
#     expected="CNMSshvol20210427.txt",
#     source_fname="CNMSshvol20210427.txt",
#     source_addr_base="http://regsho.finra.org/",
# )
# sec_ftd_1 = FakeDataItem(
#     expected="cnsfails202103a.txt",
#     source_fname="cnsfails202103a.zip",
#     source_addr_base="https://www.sec.gov/files/data/fails-deliver-data/",
# )

# class FakeData:
#     items = []
#     def add(self, item):
#         self.items.append(item)
#     def get():
#         pass
