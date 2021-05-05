import click
from datetime import datetime, timedelta
import cli
import stonks
from launcher import validators, utils


# @click.group(invoke_without_command=True)
@click.group()
def main():
    """Stock data fetcher and parser.

    Retrieves data from various sources and time frame for some given symbols
    and outputs them on an output of your choice.

    If launched without any commands this message is shown.
    Each command has its own set of arguments. to know more call for example

        stonks cli --help
    """
    pass


FILE_HELP = "Path to a settings file to read and write to."
DATE_HELP = "Override and replace the set {d} date."
START_DATE_EXTRA = "You can use 'last' to set it to the day after the "


@main.command('cli')
@click.option('-f', '--settings-file', callback=validators.settings_path,
              help=FILE_HELP)
def run_interactive_cli(settings_file=None):
    """Launch the interactive cli.

    If a VALID settings file is provided it will be loaded,
    otherwise it will either load the default one, if no file is given
    or create the new settings file and start empty for you to setup.
    """
    cli.launch(settings_file)


@main.command('run')
@click.option('-f', '--settings-file', callback=validators.settings_path,
              help=(FILE_HELP), required=True)
@click.option('-s', '--start_date', help=DATE_HELP.format(d="start"))
@click.option('-e', '--end_date', help=DATE_HELP.format(d="end"))
@click.option('-p', '--show-progress', is_flag=True,
              help="Show the progress bar")
@click.option('--debug', is_flag=True,
              help="Output debug information")
def run_from_args(
      settings_file, start_date, end_date, show_progress,
      debug, *args, **kwargs):
    """Perform a run using the given settings to load.

    Note that the file is required and has to be a valid configuration file.

    When passing a date you can also use
    'last' on the start date to previous end date + 1 day and
    'today' on the end day to set it to the current date
    """

    def dbg(txt): debug and click.echo(txt)
    def prog(txt): debug and show_progress and click.echo(txt)

    stonks.init()

    dbg(f"Loading settings from {utils.parse_path(settings_file)}")

    settings = stonks.Settings(settings_path=settings_file, debug=debug)
    app = stonks.App(settings, show_progress=show_progress, debug=debug)
    init_ok = settings.init()  # read the settings from file to modify it

    # validation done forward of handling changes and stuff
    init_ok = validate_settings(settings, settings_file, debug)

    parse_date_args(start_date, end_date, settings)

    debug and cli.utils.print_current_options(settings)

    # perform a last validation after updating the values
    init_ok = validate_settings(settings, settings_file, debug)

    if init_ok:
        execute_run(app, settings, show_progress, prog)
    else:
        click.echo("There were issues loading the settings. Bailing.")


def execute_run(app, settings, show_progress, proglog):
    if show_progress:
        cleaner = cli.utils.run_cleaner(
            settings, current_settings=False, clear_screen=False)
        cleaner()

    for _ in app.run():
        pass  # do nothing, just iterate through the generator
    show_progress and cleaner and cleaner()

    proglog(utils.parse_path(settings.output_path))
    app.settings.to_file()


def validate_settings(settings, path, debug):
    # TODO: Replace with method inside settings
    if not cli.utils.validate_settings(settings, debug):
        # TODO: Proper logging please!
        print(f"{utils.parse_path(path)} or"
              " arguments had issues. please check.")
        click.Abort()
    return True


def parse_start_date_arg(date, settings):
    """Parse the start date including 'last' word to get a new file. """
    if date == 'last':
        return (settings.end_date + timedelta(days=1)).strftime('%Y-%m-%d')
    return date


def parse_end_date_arg(date, settings):
    """Parse our end date including our 'today' word."""
    if date == 'today':
        return datetime.now().date().strftime('%Y-%m-%d')
    return date


def parse_date_args(start, end, settings):
    # process end dates
    try:
        if start:
            settings.start_date = parse_start_date_arg(start, settings)
    except stonks.exceptions.DateException:
        click.echo(
            "Wrong date format passed for START DATE. use one of "
            ', '.join(settings.VALID_DATES_FORMAT))
    try:
        if end:
            settings.end_date = parse_end_date_arg(end, settings)
    except stonks.exceptions.DateException:
        click.echo(
            "Wrong date format passed for END DATE. use one of "
            ', '.join(settings.VALID_DATES_FORMAT))
