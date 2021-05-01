import csv
import time
import click
from termcolor import colored
from simple_term_menu import TerminalMenu
from cli import utils

from scraper.components import manager


def get_menu():
    return [
        ("[x] Back", utils.handle_go_back),
        ("[t] Change output file type", handle_output_type),
        ("[p] Change output path", handle_output_path),
        ("[f] Change output file format", handle_output_filename),
        ("[d] Change CSV format", handle_csv_dialect),
    ]


def description():
    type_ = utils.highlight("outputy type")
    path_ = utils.highlight("path")
    frmt = utils.highlight("format")
    return ("Specify the options for the output of the scraping.\n"
            f"In {type_} you can define your data format\n"
            f"In {path_} you can customize your output folder\n"
            f"In {frmt} can customize your filename format (n/a right now)\n")


def run(settings):
    utils.run_menu(get_menu(), settings, "Edit output", description())


def out_type_descr():
    file = utils.highlight("single file")
    ticker = utils.highlight("single ticker")
    symbol = utils.highlight('symbol')
    return (f"You can choose to output as {file} or {ticker}.\n"
            f"- {file}   will dump all the scraped data into a single file,\n"
            "  mantaining all the columns in the source file\n"
            f"- {ticker} will generate one file for each ticker ({symbol})\n"
            "  and will remove the ticker itself from the data.\n")


def handle_output_type(settings):
    utils.pre_menu(settings, "Change output Type", out_type_descr())

    output_type_items = (utils.BACK_TXT, *manager.get_outputs())

    output_menu = TerminalMenu(
        menu_entries=[option for option in output_type_items])

    choice = output_menu.show()
    click.echo(output_type_items)
    try:
        settings.output_type = output_type_items[choice]
    except Exception:
        pass

    return False


def csv_dialect_desc():
    return "Select one of the avilable formats to format your data.\n"


def handle_csv_dialect(settings):
    utils.pre_menu(settings, "Change CSV format", csv_dialect_desc())

    # add default dialects since they are available
    csv_format_items = (
        utils.BACK_TXT,
        *manager.get_dialects_list(),
        *csv.list_dialects()
    )

    csv_menu = TerminalMenu(
        menu_entries=csv_format_items,
        cursor_index=csv_format_items.index(settings.csv_out_dialect)
        )
    choice = csv_menu.show()

    if choice == utils.BACK_TXT:
        return False

    try:
        settings.csv_out_dialect = csv_format_items[choice]
    except Exception:
        pass

    return False


def out_path_descr():

    def ext(x):
        return utils.highlight(x)

    return (f"Your desired path.\nIf a file extention ({ext('.csv')}"
            f"or {ext('.txt')}) is found that will be used as filename\n"
            "otherwise thefilename will be generated automatically.\n")


def handle_output_path(settings):
    utils.pre_menu(settings, "Set output Path", out_path_descr())

    path = click.prompt("Type your base path", default=settings.output_path)
    settings.output_path = path
    return False


def out_frmt_descr():
    return """In the future you can specify a completely custom file or a formatting
for the generated data. For now this functionality is disabled.
"""


def handle_output_filename(settings):

    utils.pre_menu(
        settings, colored("Feature coming soon", "red"), out_frmt_descr())
    time.sleep(1)
    return False
