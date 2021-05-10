import click
from termcolor import colored
from simple_term_menu import TerminalMenu

from stonks import manager, exceptions
import utils

from cli.helpers.handlers import HandlersMenuItems  # noqa


BACK_TXT = '[ BACK ]'
ESC_HINT = "Press {ESC:yellow} to go back"


def noop(): return False


def is_list(o):
    return type(o) is list


def get_choices(menu_items):
    return [item[0] for item in menu_items]


def handle_choice(menu_items, choice, settings):
    try:
        return menu_items[choice][1](settings)
    except Exception:
        return True


def run_menu(menu_items, settings, header=None, description=None):

    menu_exit = False
    menu = TerminalMenu(get_choices(menu_items))

    while not menu_exit:
        pre_menu(settings, header, description)

        choice = menu.show()
        menu_exit = handle_choice(menu_items, choice, settings)


def print_current_options(settings):
    click.echo(utils.cli.highlight("Current Options"))
    items = settings.serialize()
    del items['settings_path']  # for now at least we don't want to show this

    # Get the handlers from the manager to match the settings value with
    # the proper connected text
    mi_sh = HandlersMenuItems(manager.get_all_handlers())
    mi_wh = HandlersMenuItems(manager.get_all_writers())

    for k, v in items.items():
        if k == 'Type':
            v = mi_wh.get_name_by_value(v)
        elif k == 'Sources' and is_list(v):
            v = [mi_sh.get_name_by_value(x) for x in v]
        if type(v) is list:  # beautify lists
            v = ', '.join(v)

        click.echo("{}\t{}".format(
            colored(k, 'cyan'), colored(v, attrs=['bold'])))


def pre_menu(
      settings, header=None, description=None,
      current=True, clear=True, *args, **kwargs):

    clear and click.clear()
    current and print_current_options(settings)
    current and print()
    if header:
        click.echo(colored("{}\n".format(header), 'yellow', attrs=['bold']))
    if description:
        click.echo(description)
    validate_settings(settings)


def set_date(settings, default, field_name, header=None, description=None):
    is_done = False
    while not is_done:
        pre_menu(settings, header, description)
        try:
            datestr = click.prompt(
                "Enter your date", default=default.strftime("%Y-%m-%d"))

            if field_name == 'start_date':
                settings.start_date = datestr
            elif field_name == 'end_date':
                settings.end_date = datestr
            else:
                raise ValueError(
                    "Wrong Field name provided to cli.cli:set_date")
            is_done = True
        except exceptions.DateException:
            click.echo(utils.cli.format(
                "\n{Invalid format:red}. Should be one of "
                f"{get_date_format_str(settings)}\n"))
            if not click.confirm("Invalid date format, Try again?"):
                is_done = True


def validate_dates(settings):
    if not settings.start_date or not settings.end_date:
        return False
    # dates should be in the correct order.
    return ((settings.end_date - settings.start_date).days >= 0)


def validate_settings(settings, echo=True):

    def echo_error(error):
        echo and click.echo(utils.cli.highlight(error, "red"))
        return False

    ok = settings.validate()
    for error in settings.errors:
        echo_error(error)

    # add blank line if errors where print and we are actually writing stuff
    (not ok and echo) and click.echo()
    return ok


def get_date_format_str(settings):
    return ', '.join(
        [utils.cli.highlight(f, 'cyan') for f in settings.VALID_DATES_FORMAT])


class run_cleaner:
    def __init__(self, settings, current_settings=True, clear_screen=True):

        self.sources = HandlersMenuItems(
            manager.get_all_handlers()).get_friendly_names(
                lambda s: s.v in settings.sources)

        self.it = 0
        self.settings = settings
        self.count = len(self.sources)
        self.source_name = ''
        self.pm_kwargs = {'current': current_settings, 'clear': clear_screen}

    def __call__(self):
        if self.it == len(self.sources):
            return self.it, self.sources[self.it-1]
        try:    # with this logic the last call goes out of range, so this.
            self.source_name = utils.cli.highlight(self.sources[self.it])
            self.it += 1
        except IndexError:
            pass

        pre_menu(
            settings=self.settings,
            header=(f"Please Wait, I'm working on {self.source_name}"
                    f" ({self.it}/{self.count})"),
            **self.pm_kwargs,
        )

        return (self.it, self.source_name)
