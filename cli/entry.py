import os
import time
import click
from simple_term_menu import TerminalMenu
from termcolor import colored
from cli import utils, tickers, output, dates, sources
from scraper import StockScraper


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
    R = utils.highlight("R")
    run = utils.highlight("run the scraper")
    return (
f"""You can change the various settings from the menu or it {R} to {run}.
Changes to the settings are saved to file when youx exit the program.

Explore the various options to see how to change parameters and what they do.
"""
)

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
        click.echo(utils.highlight("Run aborted. There are missing required settings."))
        time.sleep(3)
        return

    scraper = StockScraper(settings)
    scraper.run()
    # TODO: Find a way to show this message
    out_folder = utils.highlight(os.path.abspath(settings.output_path))
    utils.pre_menu(settings, f"All Done! you can file your output in\n{out_folder}")

def handle_exit(settings):
    settings.to_file()
    utils.pre_menu(settings,"Goodbye!")
    return True
