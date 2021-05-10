import csv
import click

from simple_term_menu import TerminalMenu

import utils
from stonks import manager
from cli.helpers import Page, Menu, HandlersMenuItems


def handle_output_type(settings):
    menu_items = HandlersMenuItems(manager.get_all_writers())

    output_menu = TerminalMenu(
        menu_entries=menu_items.get_friendly_names(),
        cursor_index=menu_items.get_choice_index(settings.output_type),
        preview_command=menu_items.get_description_by_value
        )

    choice = output_menu.show()
    try:
        settings.output_type = menu_items.get_value(choice)
    except Exception:
        pass

    return False


def handle_csv_dialect(settings):
    # Get all the registered dialects, either on the csv module or in our
    # manager, removing duplicates if necessary.
    # As the manager is working now (21/5/1) the manger's list should be
    # already included in the list from csv module, but this ensure consistency
    csv_format_items = tuple(sorted(
        dict.fromkeys((*manager.get_dialects_list(), *csv.list_dialects()))
    ))

    csv_menu = TerminalMenu(
        menu_entries=csv_format_items,
        cursor_index=csv_format_items.index(settings.csv_out_dialect)
        )
    choice = csv_menu.show()

    try:
        settings.csv_out_dialect = csv_format_items[choice]
    except Exception:
        pass

    return False


def handle_output_path(settings):
    path = click.prompt("Type your base path", default=settings.output_path)
    settings.output_path = path
    return False


def out_frmt_descr():
    return (
        "In the future you can specify a completely custom file or a"
        " formatting for the generated data.\n"
        "For now this functionality is disabled.")


def handle_output_filename(settings):
    click.pause()
    return False


menu = Menu(
    "Edit output options",
    ("Specify the options for the output of the scraping.\n"
     "- {type:cyan}\t Define how the data is written on file(s)\n"
     "- {path:cyan}\t Customize your output folder.\n"
     "- {format:cyan} Change your filename format (n/a right now)\n"))

menu.add_child("[t] Change output file type", Page(
    "Change output Type",
    ("Select one of the available way to write your data.\n"
     "This will likely change how the data is handled when being "
     "downloaded and parsed.\n"),
    handle_output_type))

menu.add_child("[p] Change output path", Page(
    "Set output Path",
    ("Your desired path.\nIf a file extention (.{csv:yellow} "
     "or .{txt:yellow}) is found that will be used as filename\n"
     "otherwise the filename will be generated automatically by settings.\n"
     "\n{NOTE:yellow}:   you can use {~:cyan|bold} for your home folder.\n"
     "\tand a {dot:cyan|bold} (.) for the local folder."),
    handle_output_path))

menu.add_child("[f] Change output file format", Page(
    utils.cli.format("Feature coming soon", 'red'),
    ("In the future you can specify a completely custom file or a"
     " formatting for the generated data.\n"
     "For now this functionality is disabled."),
    handle_output_filename))

menu.add_child("[d] Change CSV format", Page(
    "Change CSV format",
    "Select one of the available formats to format your data.",
    handle_csv_dialect))
