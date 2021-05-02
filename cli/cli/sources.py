import time
import click
from simple_term_menu import TerminalMenu
from cli import utils

from stonks import manager


def get_menu():
    return [
        ("[x] Back", utils.handle_go_back),
        ("[a] Add sources", handle_add_sources),
        ("[r] Remove sources", handle_remove_source),
    ]


def description():
    finra = utils.highlight('FINRA Short')
    sec = utils.highlight('SEC FTD')

    return ("Select one or more sources to get data from.\n"
            f"- {finra} contains total volume and short volumes\n"
            "  from the sources they track."
            " They are reported daily after market close.\n"
            f"- {sec} contains reports on Fail to deliver.\n")


def run(settings):
    utils.run_menu(get_menu(), settings, "Edit Sources", description())


def get_sources_menu(settings, insert_mode):
    """
    @returns tuple (menu, has_content)
    """
    selected_sources = settings.sources

    if insert_mode:
        # remove the already present sources from the list
        all_sources = manager.get_sources()
        sources = set(all_sources) ^ set(selected_sources)
    else:
        # use the currently selected sources as list
        sources = selected_sources

    has_content = len(sources) > 0

    menu = TerminalMenu(
        (utils.BACK_TXT, *sources),
        multi_select=True,
        show_multi_select_hint=True,
    )
    return menu, has_content


def handle_add_sources(settings):
    menu, has_content = get_sources_menu(settings, True)
    if not has_content:
        click.echo(utils.highlight("All available sources already added."))
        time.sleep(1)
        return False

    menu.show()

    if menu.chosen_menu_entries is not None:
        try:
            for source in menu.chosen_menu_entries:
                settings.add_source(source)
        except Exception:
            pass

    return False


def handle_remove_source(settings):
    menu, has_content = get_sources_menu(settings, False)
    if not has_content:
        click.echo(utils.highlight("Source list is empty.", 'red'))
        time.sleep(1)
        return False

    menu.show()

    if menu.chosen_menu_entries is not None:
        for source in menu.chosen_menu_entries:
            settings.remove_source(source)

    return False
