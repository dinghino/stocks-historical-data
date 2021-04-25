import click
from simple_term_menu import TerminalMenu

from cli import utils, tickers
from scraper import StockScraper


main_menu_items = [
    "[s] Change Start Date", "[e] Change End Date",
    "[t] Select Tickers (empty for all)",
    "[o] Change output type",
    "[p] Change Output path",
    "[r] Run scraper",
    "[x] Save and Exit",
    ]

def run(settings):
    main_menu_exit = False

    main_menu = TerminalMenu(menu_entries=main_menu_items)

    while not main_menu_exit:
        pre_menu(settings)
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
        handle_output_type(settings)
    if choice == 4:
        return handle_output_path(settings)
    if choice == 5:
        return handle_run_scraper(settings)
    if choice == 6:
        return handle_exit(settings)

def pre_menu(settings):
    click.clear()
    utils.print_current_options(settings)
    print()

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

def handle_output_type(settings):
    print("Change Output Type")
    
    output_type_items = [
        (settings.OUTPUT_TYPE.SINGLE_FILE, "[s] single file"),
        (settings.OUTPUT_TYPE.SINGLE_TICKER, "[t] ticker files")
    ]
    output_menu = TerminalMenu(menu_entries= [txt for (v, txt) in output_type_items])
    choice = output_menu.show()
    settings.output_type = output_type_items[choice][0]
    return False

def handle_output_path(settings):
    print("Change destination path")
    path = click.prompt("Type your base path", default=settings.output_path)
    settings.output_path = path
    return False

def handle_run_scraper(settings):
    scraper = StockScraper(settings)
    print()
    scraper.run()
    return False

def handle_exit(settings):
    settings.to_file()
    return True
