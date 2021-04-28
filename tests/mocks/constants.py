import os

URL = {
    "FINRA_SHORT" : "http://regsho.finra.org/CNMSshvol20210427.txt",
    "SEC_FTD" : "https://www.sec.gov/files/data/fails-deliver-data/cnsfails202103b.zip",
}
DATES = {
    "start": "",
    "end": "",
}
SETTINGS_PATH= os.path.abspath("./tests/mocks/options.json")
TEMP_TO_FILE= os.path.abspath("./tests/mocks/temp.json")
