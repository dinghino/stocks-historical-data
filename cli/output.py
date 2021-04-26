import time
import click
from termcolor import colored
from simple_term_menu import TerminalMenu
from cli import utils

output_menu_items = [
    "[t] Change output file type",
    "[p] Change output path",
    "[f] Change output format",
    "[x] Back"
]

def run(settings):
    output_menu_back = False
    
    output_menu = TerminalMenu(output_menu_items)


    while not output_menu_back:
        utils.pre_menu(settings, "Edit output settings")

        output_menu_back = handle(output_menu.show(), settings)

def handle(choice, settings):
    if choice == 0:
        return handle_output_type(settings)
    if choice == 1:
        return handle_output_path(settings)
    if choice == 2:
        return handle_output_format(settings)
    if choice == 3:
        return True

def handle_output_type(settings):
    print("Change Output Type")
    
    output_type_items = [
        (settings.OUTPUT_TYPE.SINGLE_FILE, "[s] single file"),
        (settings.OUTPUT_TYPE.SINGLE_TICKER, "[t] ticker files")
    ]
    output_menu = TerminalMenu(menu_entries= [txt for (_, txt) in output_type_items])
    choice = output_menu.show()
    settings.output_type = output_type_items[choice][0]
    return False

def handle_output_path(settings):
    print("Change destination path")
    path = click.prompt("Type your base path", default=settings.output_path)
    settings.output_path = path
    return False

def handle_output_format(settings):
        utils.pre_menu(settings, colored("Feature coming soon", "red"))
        time.sleep(1)
        return False
