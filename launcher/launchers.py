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
DATE_HELP = "Overrides and replaces the {d} date."


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
@click.argument('settings-file', callback=validators.settings_path,
                required=True)
@click.option('-s', '--start-date', help=DATE_HELP.format(d="start"))
@click.option('-e', '--end-date', help=DATE_HELP.format(d="end"))
@click.option('-v', '--verbose', count=True,
              help="Verbosity level.")
def run_from_args(settings_file, start_date, end_date, verbose):
    """Perform a run using the given settings to load.\n
    Settings file can be absolute or relative path (with . and ~) to a valid
    application json settings file.\n
    When passing a date you can also use:\n
    - 'last' on the start date to previous end date + 1 day\n
    - 'today' on the end day to set it to the current date

    Verbosity levels:\n
    - 1 shows the progress bar\n
    - 2 shows the settings info\n
    - 3 Shows debugging information
    """

    # utility to check verbosity
    NORMAL = 1
    INFO = 2
    DEBUG = 3
    def _verbose(v): return verbose >= v

    stonks.manager.init()

    _verbose(DEBUG) and click.echo(
        f"Loading settings from {utils.parse_path(settings_file)}")

    settings = stonks.Settings(
        settings_path=settings_file, debug=_verbose(DEBUG))
    app = stonks.App(
        settings, show_progress=_verbose(NORMAL), debug=_verbose(DEBUG))
    init_ok = settings.init()  # read the settings from file to modify it

    # validation done forward of handling changes and stuff
    init_ok = validate_settings(settings, settings_file, _verbose(DEBUG))

    parse_date_args(start_date, end_date, settings)

    _verbose(2) and cli.utils.print_current_options(settings)

    # perform a last validation after updating the values
    init_ok = validate_settings(settings, settings_file, _verbose(INFO))

    if init_ok:
        execute_run(app, settings, _verbose(NORMAL), _verbose(NORMAL))
    else:
        click.echo("There were issues loading the settings. Bailing.")


def execute_run(app, settings, show_progress, verbose):
    if show_progress:
        cleaner = cli.utils.run_cleaner(
            settings, current_settings=False, clear_screen=False)
        cleaner()

    for _ in app.run():
        pass  # do nothing, just iterate through the generator
    show_progress and cleaner and cleaner()

    verbose == 2 and click.echo(utils.parse_path(settings.output_path))
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
