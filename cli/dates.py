from datetime import datetime
import click
from stonks import exceptions
from cli.helpers import Page, Menu
import utils


def handle_start_date(settings):
    if settings.start_date is None:
        default_date = datetime(2020, 5, 1).date()
    else:
        default_date = settings.start_date

    set_date(settings, default_date, 'start_date', "Change Start Date")

    return False


def handle_end_date(settings):
    if settings.end_date is None:
        default_date = datetime.now().date()
    else:
        default_date = settings.end_date

    # try:
    set_date(settings, default_date, 'end_date', "Change End Date")
    return False


def set_date(settings, default, field_name, header=None):
    is_done = False
    while not is_done:
        try:
            datestr = click.prompt(
                "Enter your date", default=default.strftime("%Y-%m-%d"))

            if field_name == 'start_date':
                settings.start_date = datestr
            elif field_name == 'end_date':
                settings.end_date = datestr
            else:
                raise ValueError(
                    "Wrong Field name provided to cli.cli:set_date")
            is_done = True
        except exceptions.DateException:
            formats = ', '.join([
                utils.cli.highlight(f, 'cyan')
                for f in settings.VALID_DATES_FORMAT
                ])

            click.echo(utils.cli.format(
                "\n{Invalid format:red}. Should be one of "f"{formats}\n"))
            if not click.confirm("Invalid date format, Try again?"):
                is_done = True


menu = Menu(
    'Setup your date range',
    ("Here you can specify your date range, that will be between"
     "your {start:cyan} and {end:cyan} dates."))

menu.add_child("[s] Change Start date", Page(
    "Change Start Date",
    "Start date must be {before:white|bold} the {end:cyan} date",
    handle_start_date))

menu.add_child("[e] Change End date", Page(
    "Change End Date",
    "End date must be {before:white|bold} the {start:cyan} date",
    handle_end_date))
