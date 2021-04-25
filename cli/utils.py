import click
from termcolor import colored
from datetime import datetime


def print_current_options(settings):
    click.echo(colored("Current Options", "cyan", attrs=['bold']))
    for k, v in settings.serialize().items():
        click.echo("{}\t{}".format(colored(k, 'cyan'), colored(v, attrs=['bold'])))

def set_date(settings, default_date, field_name):
    is_done = False
    while not is_done:
        try:
            datestr = click.prompt("Enter your date", default=default_date.strftime("%Y-%m-%d"))
            if field_name == 'start_date':
                settings.start_date = datestr
            elif field_name == 'end_date':
                settings.end_date = datestr
            else:
                raise ValueError("Wrong Field name provided to cli.cli:set_date")
            is_done = True
        except Settings.DateException as e:
            print(e)
            if not click.confirm("Invalid date format, Try again?"):
                is_done = True
