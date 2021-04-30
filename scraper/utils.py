import csv
from scraper.settings import constants

def path_contains_filename(path):
    if path[-4:] in ['.csv', '.txt']:
        return True
    return False


def register_custom_csv_dialects():
    csv.register_dialect(
        constants.CSV_OUT_DIALECTS.DEFAULT,
        delimiter="|",
        quoting=csv.QUOTE_MINIMAL
    )

