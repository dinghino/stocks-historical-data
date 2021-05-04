import time
import click
from simple_term_menu import TerminalMenu
from cli import utils

from stonks import manager


def get_menu():
    return [
        ("[a] Add sources", handle_add_sources),
        ("[r] Remove sources", handle_remove_source),
    ]


def description():
    return utils.fmt.format(
        "Select one or more sources to get data from.\n"
        "Each source will be processed {individually:cyan}"
        " and at least one file  will be created for each one of them.\n")


def run(settings):
    utils.run_menu(get_menu(), settings, "Edit Sources", description())


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

    items = utils.get_menuitems_text(menuitems, lambda i: i.v in sources)

    menu = TerminalMenu(
        items,
        multi_select=True,
        show_multi_select_hint=True,
        preview_command=utils.get_description_by_text(menuitems),
    )
    return menu, has_content


def handle_add_sources(settings):
    mi = utils.get_menuitems_for_handlers(manager.get_all_handlers())

    menu, has_content = get_sources_menu(mi, settings, True)
    if not has_content:
        click.echo(utils.highlight("All available sources already added."))
        time.sleep(1)
        return False

    menu.show()

    if menu.chosen_menu_entries is not None:
        try:
            for source in menu.chosen_menu_entries:
                settings.add_source(utils.get_value_by_text(mi, source))
        except Exception:
            pass

    return False


def handle_remove_source(settings):
    mi = utils.get_menuitems_for_handlers(manager.get_all_handlers())

    menu, has_content = get_sources_menu(mi, settings, False)
    if not has_content:
        click.echo(utils.highlight("Source list is empty.", 'red'))
        time.sleep(1)
        return False

    menu.show()

    if menu.chosen_menu_entries is not None:
        for source in menu.chosen_menu_entries:
            settings.remove_source(utils.get_value_by_text(mi, source))

    return False
