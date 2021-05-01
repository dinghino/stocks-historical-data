import click
from simple_term_menu import TerminalMenu
from cli import utils


def get_menu():
    return [
        ("[x] Back", utils.handle_go_back),
        ("[a] Add ticker(s)", handle_add_tickers),
        ("[r] Remove Ticker(s)", handle_remove_tickers),
        ("[c] clear all", handle_clear_all),
    ]


def run(settings):
    utils.run_menu(
        get_menu(),
        settings,
        "Edit Tickers list\nLeave empty to get all available")


def add_tickers_descr():
    ticker = utils.highlight('tickers')
    symbol = utils.highlight('symbols')
    space = utils.highlight('empty space')
    wrong = utils.highlight('wrong', 'red')

    return (f"Type the {ticker}/{symbol} you are interested in, spearated"
            f" by a space.\nIf a ticker does not exist or is typed {wrong}"
            "it will be skipped.\n\n"
            f"To exit in case of an error type a {space} and confirm.\n")


def handle_add_tickers(settings):
    utils.pre_menu(settings, "Add Tickers", add_tickers_descr())
    tickers_list = click.prompt("Your tickers")
    for ticker in tickers_list.split():
        settings.add_ticker(ticker)

    return False


def rm_tickers_descr():
    exit_ = utils.highlight("exit")
    cancel = utils.highlight(utils.BACK_TXT)
    return (f"Select the tickers you want to remove and confirm.\n"
            f"To {exit_} without changing anything"
            f" select {cancel} at the bottom of the list\n")


def handle_remove_tickers(settings):

    utils.pre_menu(settings, "Remove Tickers", rm_tickers_descr())

    remove_tickers_menu = TerminalMenu(
        # the Cancel is required to go back without modifying the list
        settings.tickers + [utils.BACK_TXT],
        multi_select=True,
        show_multi_select_hint=True,
    )

    remove_tickers_menu.show()

    if len(remove_tickers_menu.chosen_menu_entries) > 0:
        for ticker in remove_tickers_menu.chosen_menu_entries:
            settings.remove_ticker(ticker)

    return False


def clear_tickers_descr():
    return utils.highlight(
        "This will remove all the tickers from the list.", 'red')


def handle_clear_all(settings):
    utils.pre_menu(settings, "Clear tickers", clear_tickers_descr())
    sure = click.confirm("Are you sure", default=False)
    if sure:
        settings.clear_tickers()

    return False
