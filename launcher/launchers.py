import click
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
@click.option('-p', '--show-progress', is_flag=True,
              help="Show the progress bar")
@click.option('--debug', is_flag=True,
              help="Output debug information")
def run_from_args(settings_file, show_progress, debug, *args, **kwargs):
    """Perform a run using the given settings to load.

    Note that the file is required and has to be a valid configuration file.
    """

    def dbg(txt): debug and click.echo(txt)
    def prog(txt): debug and show_progress and click.echo(txt)

    stonks.init()

    dbg(f"Loading settings from {utils.parse_path(settings_file)}")

    settings = stonks.Settings(settings_path=settings_file, debug=debug)
    app = stonks.App(settings, show_progress=show_progress, debug=debug)
    init_ok = settings.init()

    if show_progress:
        cleaner = cli.utils.run_cleaner(
            settings, current_settings=False, clear_screen=False)
        cleaner()

    if init_ok:
        for _ in app.run():
            pass  # do nothing, just iterate through the generator
        show_progress and cleaner and cleaner()

        prog(utils.parse_path(settings.output_path))
    else:
        click.echo("There were issues loading the settings. Bailing.")
