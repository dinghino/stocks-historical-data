from datetime import datetime
import click
from stonks import exceptions
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

    set_date(
        settings, default_date,
        'start_date', "Change Start Date", description())

    return False


def handle_end_date(settings):
    if settings.end_date is None:
        default_date = datetime.now().date()
    else:
        default_date = settings.end_date

    # try:
    set_date(
        settings, default_date, 'end_date', "Change End Date", description())
    return False


def set_date(settings, default, field_name, header=None, description=None):
    is_done = False
    while not is_done:
        helpers.pre_menu(settings, header, description)
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
            click.echo(utils.cli.format(
                "\n{Invalid format:red}. Should be one of "
                f"{get_date_format_str(settings)}\n"))
            if not click.confirm("Invalid date format, Try again?"):
                is_done = True


def get_date_format_str(settings):
    return ', '.join(
        [utils.cli.highlight(f, 'cyan') for f in settings.VALID_DATES_FORMAT])
