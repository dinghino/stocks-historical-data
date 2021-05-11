import click
import utils
from stonks import App, manager

from cli import dates, helpers, output, sources, tickers


def handle_run_app(settings):
    if not helpers.functions.validate_settings(settings):
        return False

    app = App(settings, show_progress=True)
    results = []

    mi = helpers.HandlersMenuItems(manager.get_all_handlers())
    count = len(settings.sources)
    it = 0
    # run yields each source result, so we can clear the screen and start anew
    for result in app.run():
        source_name = mi.get_name_by_value(result.source)

        if result.state == App.PROCESSING:
            utils.cli.echo_divider()
            it += 1
            helpers.run.handle_processing(source_name, it, count)
        elif result.state == App.ERROR:
            helpers.run.handle_error(source_name, results)
        elif result.state == App.DONE:
            helpers.run.handle_done(source_name, results)

    helpers.run.print_outcome(settings, results)

    click.echo()
    query = "Do you want to {save:yellow} and {exit:yellow}?"
    if click.confirm(utils.cli.format(query), default=True):
        return handle_exit(settings, True)
    return False


def handle_exit(settings, save_on_exit=True):
    save_on_exit and settings.to_file()
    return True


run = helpers.Menu(
    "Main Menu",
    ("You can change the various settings from the menu "
     "or it {r:cyan|bold} to {run:yellow}."
     "\nChanges to the settings are saved to file when youx exit"
     "the program.\n\n"
     "Explore the various options to see how to change parameters"
     "and what they do.\n\n"
     f'{helpers.ESC_HINT} or cancel the selection.'))

run.add_child("[r] Run app", helpers.Page("Running...", None, handle_run_app))
run.add_child("[d] Change Date range", dates.menu)
run.add_child("[o] Change Output settings", output.menu)
run.add_child("[s] Edit sources", sources.menu)
run.add_child("[t] Edit Tickers", tickers.menu)
run.add_child("[x] Save and Exit", helpers.Page("Goodbye!", None, handle_exit))
