import time
import click
from termcolor import colored
from simple_term_menu import TerminalMenu
from cli import utils

def get_menu():
    return [
        ("[t] Change output file type", handle_output_type),
        ("[p] Change output path", handle_output_path),
        ("[f] Change output file format", handle_output_filename),
        ("[d] Change CSV format", handle_csv_dialect),
        ("[x] Back", utils.handle_go_back),
    ]
def description():
    type_ = utils.highlight("outputy type")
    path = utils.highlight("path")
    frmt = utils.highlight("format")
    return f"""Specify the options for the output of the scraping.\n"""


def run(settings):
    utils.run_menu(get_menu(), settings, "Edit output", description())

def out_type_descr():
    file = utils.highlight("single file")
    ticker = utils.highlight("single ticker")
    symbol = utils.highlight('symbol')
    return f"""You can choose to output as {file} or {ticker}.
- {file}   will dump all the scraped data into a single file,
  mantaining all the columns in the source file
- {ticker} will generate one file for each ticker ({symbol}) and will remove the
  ticker itself from the data.
"""

def handle_output_type(settings):
    utils.pre_menu(settings, "Change output Type", out_type_descr())
    
    output_type_items = [
        (settings.OUTPUT_TYPE.SINGLE_FILE, "Aggregate file"),
        (settings.OUTPUT_TYPE.SINGLE_TICKER, "Ticker files"),
        (None, utils.BACK_TXT)
    ]

    output_menu = TerminalMenu(menu_entries= [txt for (_, txt) in output_type_items])
    choice = output_menu.show()
    try:
        settings.output_type = output_type_items[choice][0]
    except:
        pass

    return False

def csv_dialect_desc():
    return f"""Select one of the avilable formats to format your data.
"""

def handle_csv_dialect(settings):
    utils.pre_menu(settings, "Change CSV format", csv_dialect_desc())
    
    csv_format_items = [
        (settings.CSV_OUT_DIALECTS.DEFAULT, "Default\tpipe as delimiter"),
        (settings.CSV_OUT_DIALECTS.EXCEL, "Excel\tcomma as delimiter"),
        (None, utils.BACK_TXT)
    ]
    csv_menu = TerminalMenu(menu_entries= [txt for (_, txt) in csv_format_items])
    choice = csv_menu.show()
    try:
        settings.csv_out_dialect = csv_format_items[choice][0]
    except:
        pass

    return False

def out_path_descr():
    def ext(x):
        return utils.highlight(x)

    return f"""Your desired path. If a file extention ({ext('.csv')} or {ext('.txt')}) is found
that will be used as filename, otherwise the filename will be generated automatically.
"""

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

    utils.pre_menu(settings, colored("Feature coming soon", "red"), out_frmt_descr())
    time.sleep(1)
    return False
