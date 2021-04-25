import os
from datetime import datetime
import time
import click
import json

from termcolor import colored
from simple_term_menu import TerminalMenu

from scraper import StockScraper

from pprint import pprint


OPTIONS_PATH = "/".join([".","data","options.json"])

DEFAULT_EMPTY_OPTIONS = {
    "Start": "",
    "End": "",
    "Type": "",
    "Path": "",
    "Tickers": [],
}

app_options = {
    "Start": "",
    "End": "",
    "Type": "",
    "Path": "",
    "Tickers": [],
}

app_output_types = [
    ("single file", "[s] single file"),
    ("ticker files", "[t] ticker files")
]


def print_current_options():
    click.echo(colored("Current Options", "cyan", attrs=['bold']))
    for k, v in app_options.items():
        click.echo("{}\t{}".format(colored(k, 'cyan'), colored(v, attrs=['bold'])))

def validate_path(path):
    if path[-1] is not "/":
        path+=("/")

    return path

# ====================== DATES== ==============================================

def set_date(default_date, field_name):
    try:
        datestr = click.prompt("Enter your date", default=default_date.strftime("%Y-%m-%d"))
        date = get_date(datestr)
        app_options[field_name] = date.strftime("%Y-%m-%d")
    except:
        if click.confirm("Invalid date format, please try again"):
            set_date(default_date, field_name)

def get_date(datestr):
    return datetime.strptime(datestr, "%Y-%m-%d").date()

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
            add_tickers()
        elif main_ticker_sel == 1:
            remove_tickers()
        elif main_ticker_sel == 2:
            app_options["Tickers"] = []
        elif main_ticker_sel == 3:
            main_ticker_menu_back = True

def add_tickers():
    tickers_list = click.prompt("Type the tickers to add, separated by spaces")
    tickers = tickers_list.upper().split()
    app_options["Tickers"].extend(tickers)

def remove_tickers():
    current_tickers = app_options["Tickers"]

    remove_tickers_menu = TerminalMenu(
        current_tickers,
        multi_select=True,
        show_multi_select_hint=True,
    )
    menu_entry_indices = remove_tickers_menu.show()
    app_options["Tickers"] = [
        t for t in current_tickers
        if t not in remove_tickers_menu.chosen_menu_entries
        ]

# ====================== RUN SCRAPER ==========================================

def run_scraper():
    scraper = StockScraper(
        single_file=True if app_options["Type"] == "single file" else False,
        tickers=app_options["Tickers"],
        base_path=app_options["Path"]
    )
    scraper.start_date = app_options["Start"]
    scraper.end_date = app_options["End"]
    scraper.run()

# ====================== OPTIONS HANDLER ======================================

def read_options():
    print("Reading options from {}".format(OPTIONS_PATH))
    
    # If path was missing (either dirs or file) create them and write empty
    # options
    if not make_fs_path(OPTIONS_PATH):
        write_options(DEFAULT_EMPTY_OPTIONS)

    # read the options from file and return the data structure
    with open(OPTIONS_PATH) as file:
        data = json.loads(file.read())

    pprint(data)
    time.sleep(2)
    return data

def write_options(options):
    with open(OPTIONS_PATH, "w") as file:
        file.write(json.dumps(options, indent=2))

def make_fs_path(path):
    if not os.path.exists(path):
        with open(OPTIONS_PATH, "w"): return True
    return False

# ====================== MAIN MENU ============================================

def main_menu():
    main_menu_exit = False
    main_menu_items = [
        "[s] Change Start Date", "[e] Change End Date",
        "[t] Select Tickers (empty for all)",
        "[o] Change output type",
        "[p] Change Output path",
        "[r] Run scraper",
        "[x] Save and Exit",
        ]

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
    )

    output_menu = TerminalMenu(
        menu_entries= [txt for (v, txt) in app_output_types]
    )

    while not main_menu_exit:

        click.clear()
        print_current_options()
        print()

        main_sel = main_menu.show()

        if main_sel == 0:                                   # Start Date
            print("Change Start Date")
            set_date(datetime(2020,5,1).date(), "Start")
        elif main_sel == 1:                                 # End Date
            print("Change End Date")
            set_date(datetime.now().date(), "End")
        elif main_sel == 2:                                 # Ticker Select
            ticker_edit_menu()
        elif main_sel == 3:                                 # Output type
            print("Change Output Type")
            out_sel = output_menu.show()
            app_options["Type"] = app_output_types[out_sel][0]
        elif main_sel == 4:                                 # Output path
            print("Change destination path")
            path = click.prompt(
                "Type your base path",
                default=app_options["Path"]
                )
            app_options["Path"] = validate_path(path)
        elif main_sel == 5:                                 # Run Scraper
            run_scraper()
            main_menu_exit = True
        elif main_sel == 6:                                 # Quit
            write_options(app_options)
            main_menu_exit = True
    
    print("Settings saved. Goodbye!")


def main():
   
    app_options = read_options()

    main_menu()


if __name__ == "__main__":
    main()
