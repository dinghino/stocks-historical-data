import os
from datetime import datetime
import time
import click
import json
import time

from termcolor import colored
from simple_term_menu import TerminalMenu

from scraper import StockScraper, Settings

from pprint import pprint

OPTIONS_PATH = "/".join([".","data","options.json"])
# Settings object for the whole app
settings = Settings()


def print_current_options():
    click.echo(colored("Current Options", "cyan", attrs=['bold']))
    for k, v in settings.serialize().items():
        click.echo("{}\t{}".format(colored(k, 'cyan'), colored(v, attrs=['bold'])))

# ====================== DATES== ==============================================

def set_date(default_date, field_name):
    is_done = False
    while not is_done:
        try:
            datestr = click.prompt("Enter your date", default=default_date.strftime("%Y-%m-%d"))
            if field_name == 'start_date':
                settings.start_date = datestr
            elif field_name == 'end_date':
                settings.end_date = datestr
            else:
                raise ValueError("Wrong Field name provided to cli.cli:set_date")
            is_done = True
        except Settings.DateException as e:
            print(e)
            if not click.confirm("Invalid date format, Try again?"):
                is_done = True


# ====================== TICKERS ==============================================

def ticker_edit_menu():
    main_ticker_menu_back = False

    tickers_main_menu = TerminalMenu(
        menu_entries=["[a] Add ticker(s)", "[r] Remove Ticker(s)", "[c] clear all", "[b] Back"],
    )

    while not main_ticker_menu_back:
        click.clear()
        print_current_options()
        print()
        print("Edit Tickers list")

        main_ticker_sel = tickers_main_menu.show()

        if main_ticker_sel == 0:
            tickers_list = click.prompt("Type the tickers to add, separated by spaces")
            for ticker in tickers_list.split():
                settings.add_ticker(ticker)

        elif main_ticker_sel == 1:
            remove_tickers_menu = TerminalMenu(
                settings.tickers,
                multi_select=True,
                show_multi_select_hint=True,
            )
            menu_entry_indices = remove_tickers_menu.show()
            if len(remove_tickers_menu.chosen_menu_entries) > 0:
                for ticker in remove_tickers_menu.chosen_menu_entries:
                    settings.remove_ticker(ticker)

        elif main_ticker_sel == 2:
            settings.clear_tickers()

        elif main_ticker_sel == 3:
            main_ticker_menu_back = True


# ====================== RUN SCRAPER ==========================================

def run_scraper():
    scraper = StockScraper(settings)
    scraper.run()

# ====================== OPTIONS HANDLER ======================================

# ====================== MAIN MENU ============================================

def main_menu():
    
    app_output_types = [
        (Settings.OUTPUT_TYPE.SINGLE_FILE, "[s] single file"),
        (Settings.OUTPUT_TYPE.SINGLE_TICKER, "[t] ticker files")
    ]

    main_menu_exit = False
    scraping_done = False
    main_menu_items = [
        "[s] Change Start Date", "[e] Change End Date",
        "[t] Select Tickers (empty for all)",
        "[o] Change output type",
        "[p] Change Output path",
        "[r] Run scraper",
        "[x] Save and Exit",
        ]

    main_menu = TerminalMenu(menu_entries=main_menu_items)

    output_menu = TerminalMenu(menu_entries= [txt for (v, txt) in app_output_types])

    while not main_menu_exit:

        click.clear()
        print_current_options()
        if scraping_done:
            print(colored("Data fetched", "red"))

        print()

        main_sel = main_menu.show()

        if main_sel == 0:                                   # Start Date
            print("Change Start Date")
            default_date = datetime(2020,5,1).date()
            # try:
            set_date(default_date, 'start_date')
            # except:
            #     print("Error while setting the date")
        elif main_sel == 1:                                 # End Date
            print("Change End Date")
            default_date = datetime.now().date()
            # try:
            set_date(default_date, 'end_date')
            # except:
            #     print("Error while setting the date")
        elif main_sel == 2:                                 # Ticker Select
            ticker_edit_menu()
        elif main_sel == 3:                                 # Output type
            print("Change Output Type")
            out_sel = output_menu.show()
            settings.output_type = app_output_types[out_sel][0]
        elif main_sel == 4:                                 # Output path
            print("Change destination path")
            path = click.prompt("Type your base path", default=settings.output_path)
            settings.output_path = path
        elif main_sel == 5:                                 # Run Scraper
            scraping_done = False
            run_scraper()
            # main_menu_exit = True
            scraping_done = True
        elif main_sel == 6:                                 # Quit
            settings.to_file(OPTIONS_PATH)
            main_menu_exit = True
    
    print("Settings saved. Goodbye!")


def main():
    os.system('clear')
    if settings.init(OPTIONS_PATH):
        print("Settings loaded")
        time.sleep(2)
        main_menu()
    else:
        print("There was an error initializing the app")


if __name__ == "__main__":
    main()
