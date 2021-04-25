import click
from simple_term_menu import TerminalMenu
from cli import utils

tickers_menu_items = [
    "[a] Add ticker(s)",
    "[r] Remove Ticker(s)",
    "[c] clear all",
    "[b] Back"
    ]

def run(settings):
    tickers_main_menu = TerminalMenu(tickers_menu_items)

    tickers_menu_back = False

    while not tickers_menu_back:
        pre_menu(settings)

        choice = tickers_main_menu.show()
        tickers_menu_back = handle(choice, settings)

def handle(choice, settings):
    if choice == 0:
        return handle_add_tickers(settings)
    elif choice == 1:
        return handle_remove_tickers(settings)
    elif choice == 2:
        return handle_clear_all(settings)
    elif choice == 3:
        return handle_go_back(settings)

def pre_menu(settings):
    click.clear()
    utils.print_current_options(settings)
    print()
    print("Edit Tickers list")

def handle_add_tickers(settings):
    tickers_list = click.prompt("Type the tickers to add, separated by spaces")
    for ticker in tickers_list.split():
        settings.add_ticker(ticker)
    
    return False

def handle_remove_tickers(settings):
    remove_tickers_menu = TerminalMenu(
        # the Cancel is required to go back without modifying the list
        settings.tickers + ["[ Cancel ]"],
        multi_select=True,
        show_multi_select_hint=True,
    )
    menu_entry_indices = remove_tickers_menu.show()
    if len(remove_tickers_menu.chosen_menu_entries) > 0:
        for ticker in remove_tickers_menu.chosen_menu_entries:
            settings.remove_ticker(ticker)
    
    return False

def handle_clear_all(settings):
    settings.clear_tickers()
    return False

def handle_go_back(settings):
    return True
