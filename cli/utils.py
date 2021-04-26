import click
from termcolor import colored
from datetime import datetime
from simple_term_menu import TerminalMenu

def get_choices(menu_items):
    return [item[0] for item in menu_items]

def handle_choice(menu_items, choice, settings):
    return menu_items[choice][1](settings)

def run_menu(menu_items, settings, header=None):

    menu_exit = False
    tickers_main_menu = TerminalMenu(get_choices(menu_items))

    while not menu_exit:
        pre_menu(settings,header)

        choice = tickers_main_menu.show()
        menu_exit = handle_choice(menu_items, choice, settings)

def handle_go_back(settings):
    return True

def print_current_options(settings):
    click.echo(colored("Current Options", "cyan", attrs=['bold']))
    for k, v in settings.serialize().items():
        click.echo("{}\t{}".format(colored(k, 'cyan'), colored(v, attrs=['bold'])))

def pre_menu(settings, header=None):
    click.clear()
    print_current_options(settings)
    print()
    if header is not None:
        print(colored("{}\n".format(header), attrs=['bold']))

def set_date(settings, default_date, field_name):
    is_done = False
    while not is_done:
        pre_menu(settings)
        try:
            datestr = click.prompt("Enter your date", default=default_date.strftime("%Y-%m-%d"))
            if field_name == 'start_date':
                settings.start_date = datestr
            elif field_name == 'end_date':
                settings.end_date = datestr
            else:
                raise ValueError("Wrong Field name provided to cli.cli:set_date")
            is_done = True
        except settings.DateException as e:
            print(e)
            if not click.confirm("Invalid date format, Try again?"):
                is_done = True
