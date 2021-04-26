import time
import click
from termcolor import colored
from simple_term_menu import TerminalMenu
from cli import utils

def get_menu():
    return [
        ("[a] Add sources", handle_add_sources),
        ("[r] Remove sources", handle_remove_source),
        ("[x] Back", utils.handle_go_back),
    ]

def run(settings):
    utils.run_menu(get_menu(), settings, "Edit Sources")

def get_sources_menu(settings, insert_mode):
    """
    @returns tuple (menu, has_content)
    """
    selected_sources = settings.sources

    if insert_mode:
        # remove the already present sources from the list
        all_sources = settings.SOURCES.VALID
        sources = sorted(list(set(all_sources) - set(selected_sources)))
    else:
        # use the currently selected sources as list
        sources = sorted(selected_sources)

    has_content = sources and len(sources) > 0

    menu = TerminalMenu(
        sources,
        multi_select=True,
        show_multi_select_hint=True,
    )
    return menu, has_content

def handle_add_sources(settings):
    menu, has_content = get_sources_menu(settings, True)
    if not has_content:
        click.echo(colored("All available sources already added.", 'red', attrs=['bold']))
        time.sleep(1)
        return False

    menu_entries = menu.show()

    if menu.chosen_menu_entries is None:
        return False

    for source in menu.chosen_menu_entries:
        settings.add_source(source)

    return False


def handle_remove_source(settings):
    menu, has_content = get_sources_menu(settings, False)
    if not has_content:
        click.echo(colored("Source list is empty.", 'red', attrs=['bold']))
        time.sleep(1)
        return False

    menu_entries = menu.show()

    if menu.chosen_menu_entries is None:
        return False

    for source in menu.chosen_menu_entries:
        settings.remove_source(source)
    return False
