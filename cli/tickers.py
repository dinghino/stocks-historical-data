import click
from termcolor import colored
from simple_term_menu import TerminalMenu
from cli import utils

def get_menu():
    return [
        ("[a] Add ticker(s)", handle_add_tickers),
        ("[r] Remove Ticker(s)", handle_remove_tickers),
        ("[c] clear all", handle_clear_all),
        ("[x] Back", utils.handle_go_back),
    ]

def run(settings):
    utils.run_menu(
        get_menu(),
        settings,
        "Edit Tickers list\nLeave empty to get all available")


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
