from datetime import datetime
from cli import utils


def get_menu():
    return [
        ("[s] Change Start date", handle_start_date),
        ("[e] Change End date", handle_end_date),
        ("[x] Back", utils.handle_go_back),
    ]


def description():
    start = utils.highlight("Start")
    end = utils.highlight("End")
    note = utils.highlight("Currently there is no check for order", 'red')

    return ("Here you can specify your date range, that will be between"
            f"your {start} and {end} dates.\n"
            f"{note}\nBe sure to have your {start} date set before in time"
            f"than the {end} date.")


def run(settings):
    utils.run_menu(get_menu(), settings, "Date Ranges", description())


def handle_start_date(settings):
    if settings.start_date is None:
        default_date = datetime(2020, 5, 1).date()
    else:
        default_date = settings.start_date

    utils.set_date(
        settings, default_date,
        'start_date', "Change Start Date", description())

    return False


def handle_end_date(settings):
    if settings.end_date is None:
        default_date = datetime.now().date()
    else:
        default_date = settings.end_date

    # try:
    utils.set_date(
        settings, default_date, 'end_date', "Change End Date", description())
    return False
