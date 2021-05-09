import click
from simple_term_menu import TerminalMenu
from cli import helpers
import utils


def get_menu():
    return [
        ("[a] Add ticker(s)", handle_add_tickers),
        ("[r] Remove Ticker(s)", handle_remove_tickers),
        ("[c] clear all", handle_clear_all),
    ]


def run(settings):
    helpers.run_menu(
        get_menu(),
        settings,
        "Edit Tickers list\nLeave empty to get all available")


def add_tickers_descr():
    return utils.cli.format(
        "Type the {tickers:cyan}/{symbols:cyan} you are interested in, spearated"  # noqa
        " by a space.\nIf a ticker does not exist or is typed {wrong:red}"
        "it will be skipped.\n\n"
        "To exit without adding anything type an {empty space:white|bold}"
        " and confirm.\n")


def handle_add_tickers(settings):
    helpers.pre_menu(settings, "Add Tickers", add_tickers_descr())
    tickers_list = click.prompt("Your tickers")
    for ticker in tickers_list.split():
        settings.add_ticker(ticker)

    return False


def rm_tickers_descr():
    return utils.cli.format(
        "Select the tickers you want to remove and confirm.\n"
        "To {exit:cyan} without changing anything.\n"
        )


def handle_remove_tickers(settings):

    helpers.pre_menu(settings, "Remove Tickers", rm_tickers_descr())

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


def clear_tickers_descr():
    return utils.cli.highlight(
        "This will remove all the tickers from the list.", 'red')


def handle_clear_all(settings):
    helpers.pre_menu(settings, "Clear tickers", clear_tickers_descr())
    sure = click.confirm("Are you sure", default=False)
    if sure:
        settings.clear_tickers()

    return False
