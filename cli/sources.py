import time
import click
from simple_term_menu import TerminalMenu

import utils
from cli import helpers
from stonks import manager


def get_menu():
    return [
        ("[a] Add sources", handle_add_sources),
        ("[r] Remove sources", handle_remove_source),
    ]


def description():
    return utils.cli.format(
        "Select one or more sources to get data from.\n"
        "Each source will be processed {individually:cyan}"
        " and at least one file  will be created for each one of them.\n")


def run(settings):
    helpers.run_menu(get_menu(), settings, "Edit Sources", description())


def get_sources_menu(menuitems, settings, insert_mode):
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

    items = menuitems.get_friendly_names(lambda i: i.v in sources)

    menu = TerminalMenu(
        items,
        multi_select=True,
        show_multi_select_hint=True,
        preview_command=menuitems.get_description_by_value,
    )
    return menu, has_content


def handle_add_sources(settings):
    mi = helpers.HandlersMenuItems(manager.get_all_handlers())

    menu, has_content = get_sources_menu(mi, settings, True)
    if not has_content:
        click.echo(utils.cli.highlight("All available sources already added."))
        time.sleep(1)
        return False

    menu.show()

    if menu.chosen_menu_entries is not None:
        try:
            for source in menu.chosen_menu_entries:
                settings.add_source(mi.get_value_by_name(source))
        except Exception:
            pass

    return False


def handle_remove_source(settings):
    mi = helpers.HandlersMenuItems(manager.get_all_handlers())

    menu, has_content = get_sources_menu(mi, settings, False)
    if not has_content:
        click.echo(utils.cli.highlight("Source list is empty.", 'red'))
        time.sleep(1)
        return False

    menu.show()

    if menu.chosen_menu_entries is not None:
        for source in menu.chosen_menu_entries:
            settings.remove_source(mi.get_value_by_name(source))

    return False
