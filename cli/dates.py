from datetime import datetime
import click
from cli import utils

def get_menu():
    return [
        ("[S] Change Start date", handle_start_date),
        ("[E] Change End date", handle_end_date),
        ("[x] Back", utils.handle_go_back),
    ]

def run(settings):
    utils.run_menu(get_menu(), settings, "Date range Settings")

def handle_start_date(settings):
    click.echo("Change Start Date")
    if settings.start_date is None:
        default_date = datetime(2020,5,1).date()
    else:
        default_date = settings.start_date

    utils.set_date(settings, default_date, 'start_date')

    return False

def handle_end_date(settings):
    click.echo("Change End Date")
    default_date = datetime.now().date()
    # try:
    utils.set_date(settings, default_date, 'end_date')
    return False
