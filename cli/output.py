import csv
import time
import click
from termcolor import colored
from simple_term_menu import TerminalMenu

import utils
from cli import helpers
from stonks import manager


def get_menu():
    return [
        ("[t] Change output file type", handle_output_type),
        ("[p] Change output path", handle_output_path),
        ("[f] Change output file format", handle_output_filename),
        ("[d] Change CSV format", handle_csv_dialect),
    ]


def description():
    return utils.cli.format(
        "Specify the options for the output of the scraping.\n"
        "- {type:cyan}\t Define how the data is written on file(s)\n"
        "- {path:cyan}\t Customize your output folder.\n"
        "- {format:cyan} Change your filename format (n/a right now)\n")


def run(settings):
    helpers.run_menu(get_menu(), settings, "Edit output", description())


def out_type_descr():
    return utils.cli.format(
        "Select one of the available way to write your data.\n"
        "This will likely change how the data is handled when being "
        "downloaded and parsed.\n"
    )


def handle_output_type(settings):
    helpers.pre_menu(settings, "Change output Type", out_type_descr())

    menu_items = helpers.HandlersMenuItems(manager.get_all_writers())

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


def csv_dialect_desc():
    return utils.cli.format(
        "Select one of the avilable formats to format your data.\n"
        )


def handle_csv_dialect(settings):
    helpers.pre_menu(settings, "Change CSV format", csv_dialect_desc())

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


def out_path_descr():
    return utils.cli.format(
        "Your desired path.\nIf a file extention (.{csv:yellow} "
        "or .{txt:yellow}) is found that will be used as filename\n"
        "otherwise the filename will be generated automatically by settings.\n"
        "\n{NOTE:yellow}: you can use {~:cyan|bold} for your home folder.\n"
        )


def handle_output_path(settings):
    helpers.pre_menu(settings, "Set output Path", out_path_descr())

    path = click.prompt("Type your base path", default=settings.output_path)
    settings.output_path = path
    return False


def out_frmt_descr():
    return (
        "In the future you can specify a completely custom file or a"
        " formatting for the generated data.\n"
        "For now this functionality is disabled.")


def handle_output_filename(settings):

    helpers.pre_menu(
        settings, colored("Feature coming soon", "red"), out_frmt_descr())
    time.sleep(1)
    return False
