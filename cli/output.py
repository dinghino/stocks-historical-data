import time
import click
from termcolor import colored
from simple_term_menu import TerminalMenu
from cli import utils

def get_menu():
    return [
        ("[t] Change output file type", handle_output_type),
        ("[p] Change output path", handle_output_path),
        ("[f] Change output format", handle_output_format),
        ("[x] Back", utils.handle_go_back),
    ]

def run(settings):
    utils.run_menu(get_menu(), settings, "Edit output settings")

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
