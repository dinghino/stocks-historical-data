import csv
# from scraper.settings import constants


def path_contains_filename(path):
    if path[-4:] in ['.csv', '.txt']:
        return True
    return False


# def register_custom_csv_dialects():
#     csv.register_dialect(
#         constants.CSV_OUT_DIALECTS.DEFAULT,
#         delimiter="|",
#         quoting=csv.QUOTE_MINIMAL
#     )


# TODO: Replace original function, this is just for testing purpose
def register_custom_csv_dialects(data):
    for name, args in data:
        csv.register_dialect(name, **args)
