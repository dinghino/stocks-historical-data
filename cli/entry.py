import click
from simple_term_menu import TerminalMenu
from cli import utils, tickers, output
from scraper import StockScraper


main_menu_items = [
    "[s] Change Start Date",
    "[e] Change End Date",
    "[t] Edit Tickers",
    "[o] Change output settings",
    "[r] Run scraper",
    "[x] Save and Exit",
    ]

def run(settings):
    main_menu_exit = False

    main_menu = TerminalMenu(menu_entries=main_menu_items)

    while not main_menu_exit:
        utils.pre_menu(settings)
        choice = main_menu.show()
        main_menu_exit = handle(choice, settings)

def handle(choice, settings):
    if choice == 0:
        return handle_start_date(settings)
    if choice == 1:
        return handle_end_date(settings)
    if choice == 2:
        tickers.run(settings)
    if choice == 3:
        output.run(settings)
    if choice == 4:
        return handle_run_scraper(settings)
    if choice == 5:
        return handle_exit(settings)

def handle_start_date(settings):
    print("Change Start Date")
    if settings.start_date is None:
        default_date = datetime(2020,5,1).date()
    else:
        default_date = settings.start_date

    utils.set_date(settings, default_date, 'start_date')

    return False

def handle_end_date(settings):
    print("Change End Date")
    default_date = datetime.now().date()
    # try:
    utils.set_date(settings, default_date, 'end_date')
    return False

def handle_run_scraper(settings):
    scraper = StockScraper(settings)
    print()
    scraper.run()
    return False

def handle_exit(settings):
    settings.to_file()
    return True
