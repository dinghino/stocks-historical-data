from datetime import datetime, timedelta

import cli
import click
import stonks
import utils
from loguru import logger

from launcher import validators


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
@click.option('-f', '--settings-file', callback=validators.settings_path(True),
              help=FILE_HELP)
def run_interactive_cli(settings_file):
    """Launch the interactive cli.

    If a VALID settings file is provided it will be loaded,
    otherwise it will either load the default one, if no file is given
    or create the new settings file and start empty for you to setup.
    """
    cli.launch(settings_file)


@main.command('run')
@click.argument('file-path', callback=validators.settings_path(),
                required=True)
@click.option('-s', '--start-date', help=DATE_HELP.format(d="start"))
@click.option('-e', '--end-date', help=DATE_HELP.format(d="end"))
@click.option('-v', '--verbose', count=True,
              help="Verbosity level.")
def run_from_args(file_path, start_date, end_date, verbose):
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
    VERBOSE = 3
    DEBUG = 4
    def lvl(v): return verbose >= v

    path = utils.path.parse(file_path)
    lvl(DEBUG) and click.echo(f"Loading settings from {path}")

    stonks.manager.init()
    settings = stonks.Settings(settings_path=file_path, debug=lvl(DEBUG))
    init_ok = settings.init()  # read the settings from file to modify it

    init_ok = pre_run(settings, start_date, end_date)

    # validation done forward of handling changes and stuff
    abort_fail(validate_settings, settings, lvl(DEBUG))

    abort_fail(parse_date_args, start_date, end_date, settings)

    lvl(INFO) and cli.helpers.functions.print_current_options(settings)

    if init_ok:
        run_app(settings, lvl(NORMAL), lvl(INFO), lvl(VERBOSE), lvl(DEBUG))
    else:
        click.echo("There were issues loading the settings. Bailing.")


def abort_fail(func, *args, **kwargs):
    if not func(*args, **kwargs):
        click.echo("There were issues setting up")
        click.Abort()


def pre_run(settings, start, end):
    ok = parse_date_args(start, end, settings)
    return ok


def run_app(settings, normal, info, verbose, debug):
    mi = cli.helpers.HandlersMenuItems(stonks.manager.get_all_handlers())
    count = len(settings.sources)
    it = 0

    app = stonks.App(settings, show_progress=normal, debug=debug)
    results = []

    for result in app.run():
        source_name = mi.get_name_by_value(result.source)
        if result.state == stonks.App.PROCESSING:
            info and utils.cli.echo_divider()
            it += 1
            cli.helpers.run.handle_processing(source_name, it, count, info)
        elif result.state == stonks.App.ERROR:
            cli.helpers.run.handle_error(source_name, results)
        elif result.state == stonks.App.DONE:
            cli.helpers.run.handle_done(source_name, results)

    cli.helpers.run.print_outcome(settings, results, normal, False)


def validate_settings(settings, debug):
    # TODO: Replace with method inside settings
    if not settings.validate():
        (click.echo(e) for e in settings.error)
        return False
    return True


def parse_date_args(start, end, settings):
    # process end dates
    ok = True

    def parse_start(date):
        """Parse the start date including 'last' word to get a new file. """
        if date == 'last':
            return (settings.end_date + timedelta(days=1)).strftime('%Y-%m-%d')
        return date

    def parse_end(date):
        """Parse our end date including our 'today' word."""
        if date == 'today':
            return datetime.now().date().strftime('%Y-%m-%d')
        return date

    if start:
        try:
            settings.start_date = parse_start(start)
        except stonks.exceptions.DateException:
            ok = False
            logger.debug(
                "\nWrong date format passed for START DATE. use one of " +
                ', '.join(settings.VALID_DATES_FORMAT))
    if end:
        try:
            settings.end_date = parse_end(end)
        except stonks.exceptions.DateException:
            ok = False
            logger.debug(
                "\nWrong date format passed for END DATE. use one of " +
                ', '.join(settings.VALID_DATES_FORMAT))
    return ok
