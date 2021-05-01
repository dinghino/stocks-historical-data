import csv
# from scraper.settings import constants


def path_contains_filename(path):
    if path[-4:] in ['.csv', '.txt']:
        return True
    return False
