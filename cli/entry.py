import os
import time
import click
from cli import utils, tickers, output, dates, sources
from scraper import App


def get_menu():
    return [
        ("[d] Change Date range", handle_dates_menu),
        ("[o] Change Output settings", handle_output_menu),
        ("[s] Edit sources", handle_sources_menu),
        ("[t] Edit Tickers", handle_tickers_menu),
        ("[r] Run scraper", handle_run_scraper),
        ("[x] Save and Exit", handle_exit),
    ]


def description():
    R = utils.highlight("r")
    run = utils.highlight("run the scraper")
    return ("You can change the various settings from the menu "
            f"or it {R} to {run}."
            "\nChanges to the settings are saved to file when youx exit"
            "the program.\n\n"
            "Explore the various options to see how to change parameters"
            "and what they do.\n")


def run(settings):
    utils.run_menu(get_menu(), settings, "Main Menu", description())


def handle_dates_menu(settings):
    dates.run(settings)


def handle_tickers_menu(settings):
    tickers.run(settings)


def handle_output_menu(settings):
    output.run(settings)


def handle_sources_menu(settings):
    sources.run(settings)


def handle_run_scraper(settings):
    if not utils.validate_settings(settings, False):
        click.echo(utils.highlight(
            "Run aborted. There are missing required settings."))
        time.sleep(3)
        return

    scraper = App(settings, show_progress=True)
    cleaner = utils.run_cleaner(settings)
    errors = []
    # run yields each source result, so we can clear the screen and start anew
    _, source_name = cleaner()
    for result in scraper.run():
        if not result:
            err = utils.highlight(
                f"There was en error processing {source_name}", "red")
            utils.pre_menu(settings, err)
            errors.append(err)
            time.sleep(2)
            continue

        _, source_name = cleaner()

    # TODO: Find a way to show this message
    out_folder = utils.highlight(os.path.abspath(settings.output_path))

    end_desc = "You can find you data in : {}\n{}".format(
        out_folder, "\n".join(errors))

    utils.pre_menu(settings, "All Done!", end_desc)
    return handle_exit(settings, False)


def handle_exit(settings, print_msg=True):
    settings.to_file()
    print_msg and utils.pre_menu(settings, "Goodbye!")
    return True
