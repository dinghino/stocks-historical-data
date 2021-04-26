import click
from simple_term_menu import TerminalMenu
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

def run(settings):
    utils.run_menu(get_menu(), settings)

def handle_dates_menu(settings):
    dates.run(settings)

def handle_tickers_menu(settings):
    tickers.run(settings)

def handle_output_menu(settings):
    output.run(settings)

def handle_sources_menu(settings):
    sources.run(settings)

def handle_run_scraper(settings):
    scraper = StockScraper(settings)
    print()
    scraper.run()
    return False

def handle_exit(settings):
    settings.to_file()
    return True
