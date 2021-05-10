import os
import click
from cli import helpers, tickers, output, dates, sources
from stonks import App
import utils
from cli.helpers import Page, Menu


def pre_run(settings):
    if helpers.validate_settings(settings, False):
        return True
    click.echo(utils.cli.highlight(
        "Run aborted. There are missing required settings."))
    click.pause()
    return False


def handle_run_scraper(settings):
    if not pre_run(settings):
        return False

    scraper = App(settings, show_progress=True)
    # TODO: refactor cleaner. it runs the pre_menu and we don't want that
    cleaner = helpers.run_cleaner(settings)
    errors = []
    # run yields each source result, so we can clear the screen and start anew
    _, source_name = cleaner()
    for result in scraper.run():
        if not result:
            err = utils.cli.highlight(
                f"There was en error processing {source_name}", "red")
            helpers.pre_menu(settings, err)
            errors.append(err)
            click.pause()
            continue

        _, source_name = cleaner()

    out_folder = utils.cli.highlight(os.path.abspath(settings.output_path))

    end_desc = "You can find you data in : {}\n{}".format(
        out_folder, "\n".join(errors))
    helpers.pre_menu(settings, "All Done!", end_desc)

    if click.confirm(
          utils.cli.format("Do you want to {exit:yellow}?"), default=True):
        return handle_exit(settings, True)
    return False


def handle_exit(settings, print_msg=True, save_on_exit=True):
    save_on_exit and settings.to_file()
    return True


run = Menu(
    "Main Menu",
    ("You can change the various settings from the menu "
     "or it {r:cyan|bold} to {run:yellow}."
     "\nChanges to the settings are saved to file when youx exit"
     "the program.\n\n"
     "Explore the various options to see how to change parameters"
     "and what they do.\n\n"
     f'{helpers.ESC_HINT} or cancel the selection.'))

run.add_child("[r] Run scraper", Page(
    "Running", "please wait", handle_run_scraper))

run.add_child("[d] Change Date range", dates.menu)
run.add_child("[o] Change Output settings", output.menu)
run.add_child("[s] Edit sources", sources.menu),
run.add_child("[t] Edit Tickers", tickers.menu)
run.add_child("[x] Save and Exit", Page("Goodbye!", None, handle_exit))
