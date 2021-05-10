import click
from simple_term_menu import TerminalMenu

import utils
from cli.helpers import Menu, Page


def handle_add_tickers(settings):
    tickers_list = click.prompt("Your tickers")
    for ticker in tickers_list.split():
        settings.add_ticker(ticker)
    return False


def handle_remove_tickers(settings):
    remove_tickers_menu = TerminalMenu(
        settings.tickers,
        multi_select=True,
        show_multi_select_hint=True,
    )

    remove_tickers_menu.show()
    selected = remove_tickers_menu.chosen_menu_entries

    if selected and len(selected) > 0:
        for ticker in selected:
            settings.remove_ticker(ticker)
    return False


def handle_clear_all(settings):
    sure = click.confirm("Are you sure", default=False)
    if sure:
        settings.clear_tickers()
    return False


menu = Menu("Edit your tickers/symbols list")

menu.add_child("[a] Add ticker(s)", Page(
    "Add tickers",
    ("Type the {tickers:cyan}/{symbols:cyan} you are interested in, spearated"
     " by a space.\nIf a ticker does not exist or is typed {wrong:red}"
     "it will be skipped.\n\n"
     "To exit without adding anything type an {empty space:white|bold}"
     " and confirm.\n"),
    handle_add_tickers))

menu.add_child("[r] Remove Ticker(s)", Page(
    "Remove Tickers",
    ("Select the tickers you want to remove and confirm.\n"
     "To {exit:cyan} without changing anything.\n"),
    handle_remove_tickers))

menu.add_child("[c] clear all", Page(
    "Clear All tickers",
    utils.cli.highlight("This will remove ALL the tickers.", 'red'),
    handle_clear_all))
