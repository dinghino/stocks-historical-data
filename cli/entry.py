import os
import time
import click
from cli import helpers, tickers, output, dates, sources
from stonks import App
import utils


def get_menu():
    return [
        ("[r] Run scraper", handle_run_scraper),
        ("[x] Save and Exit", handle_exit),
        ("[d] Change Date range", dates.run),
        ("[o] Change Output settings", output.run),
        ("[s] Edit sources", sources.run),
        ("[t] Edit Tickers", tickers.run),
    ]


def description():
    return utils.cli.format(
        "You can change the various settings from the menu "
        "or it {r:cyan|bold} to {run:yellow}."
        "\nChanges to the settings are saved to file when youx exit"
        "the program.\n\n"
        "Explore the various options to see how to change parameters"
        "and what they do.\n\n"
        f'{helpers.ESC_HINT} or cancel the selection.\n')


def run(settings):
    helpers.run_menu(get_menu(), settings, "Main Menu", description())


def handle_run_scraper(settings):
    if not helpers.validate_settings(settings, False):
        click.echo(helpers.highlight(
            "Run aborted. There are missing required settings."))
        time.sleep(3)
        return

    scraper = App(settings, show_progress=True)
    cleaner = helpers.run_cleaner(settings)
    errors = []
    # run yields each source result, so we can clear the screen and start anew
    _, source_name = cleaner()
    for result in scraper.run():
        if not result:
            err = helpers.highlight(
                f"There was en error processing {source_name}", "red")
            helpers.pre_menu(settings, err)
            errors.append(err)
            time.sleep(2)
            continue

        _, source_name = cleaner()

    out_folder = helpers.highlight(os.path.abspath(settings.output_path))

    end_desc = "You can find you data in : {}\n{}".format(
        out_folder, "\n".join(errors))
    helpers.pre_menu(settings, "All Done!", end_desc)

    if click.confirm(
          utils.cli.format("Do you want to {exit:yellow}?"), default=True):
        return handle_exit(settings, True)
    return False


def handle_exit(settings, print_msg=True, save_on_exit=True):
    save_on_exit and settings.to_file()
    print_msg and helpers.pre_menu(settings, "Goodbye!")
    return True
