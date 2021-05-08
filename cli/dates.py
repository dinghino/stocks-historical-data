from datetime import datetime
from cli import helpers
import utils


def get_menu():
    return [
        ("[s] Change Start date", handle_start_date),
        ("[e] Change End date", handle_end_date),
    ]


def description():
    return utils.cli.format(
        "Here you can specify your date range, that will be between"
        "your {start:cyan} and {end:cyan} dates.\n\n")


def run(settings):
    helpers.run_menu(get_menu(), settings, "Date Ranges", description())


def handle_start_date(settings):
    if settings.start_date is None:
        default_date = datetime(2020, 5, 1).date()
    else:
        default_date = settings.start_date

    helpers.set_date(
        settings, default_date,
        'start_date', "Change Start Date", description())

    return False


def handle_end_date(settings):
    if settings.end_date is None:
        default_date = datetime.now().date()
    else:
        default_date = settings.end_date

    # try:
    helpers.set_date(
        settings, default_date, 'end_date', "Change End Date", description())
    return False
