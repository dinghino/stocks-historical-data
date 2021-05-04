import click
import string
from termcolor import colored, COLORS
from simple_term_menu import TerminalMenu

from stonks import manager, exceptions

BACK_TXT = '[ BACK ]'
ESC_HINT = "Press {ESC:yellow} to go back"


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
    # print("\n\nderpino, use manager here to fix the text\n\n")
    # raise Exception
    click.echo(colored("Current Options", "cyan", attrs=['bold']))
    items = settings.serialize()
    del items['settings_path']  # for now at least we don't want to show this

    # Get the handlers from the manager to match the settings value with
    # the proper connected text
    mi_sh = get_menuitems_for_handlers(manager.get_all_handlers())
    mi_wh = get_menuitems_for_handlers(manager.get_all_writers())

    for k, v in items.items():
        if k == 'Type':
            v = get_text_by_value(mi_wh, v)
        elif k == 'Sources' and is_list(v):
            v = [get_text_by_value(mi_sh, x) for x in v]
        if type(v) is list:  # beautify lists
            v = ', '.join(v)

        click.echo("{}\t{}".format(
            colored(k, 'cyan'), colored(v, attrs=['bold'])))


def pre_menu(settings, header=None, description=None):
    click.clear()
    print_current_options(settings)
    print()
    if header:
        click.echo(colored("{}\n".format(header), 'yellow', attrs=['bold']))
    if description:
        click.echo(description)
    validate_settings(settings)


def highlight(text, color='cyan', attrs=['bold']):
    return colored(text, color, attrs=attrs)


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
            click.echo(fmt.format(
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
        echo and click.echo(highlight(error, "red"))
        return False

    ok = True
    check_dates = True

    if not settings.start_date:
        ok = echo_error("Start date is required")
        check_dates = False
    if not settings.end_date:
        ok = echo_error("End date is required")
        check_dates = False
    if check_dates and not validate_dates(settings):
        ok = echo_error("Dates are in incorrect order")
    if not settings.output_path or len(settings.output_path) == 0:
        ok = echo_error("You need an output path")
    if not settings.output_type:
        ok = echo_error("Output type is missing")
    if not settings.sources or len(settings.sources) == 0:
        ok = echo_error("You need at least a source")

    if not ok:
        click.echo()
    return ok


def get_date_format_str(settings):
    return ', '.join(
        [highlight(f, 'cyan') for f in settings.VALID_DATES_FORMAT])


class MenuItem:
    def __init__(self, value, text, description):
        self.v = value
        self.t = text
        self.d = description

    def __repr__(self):
        return f'<v: {self.v} | t: {self.t} | d:{self.d}>'


def get_menuitems_for_handlers(handlers):
    """
    Takes a list of handlers from `stonks.manager` and returns a list of
    tuples containing relevant values for the cli, to be used to generate the
    UI with friendly names, match the choices to the actual values and other
    attributes registered in the handlers.

    This is required for all options that require validation with the manager,
    so all the source and writer components.
    """
    def gt(i): return getattr(i, 'source', getattr(i, 'output_type', None))

    return [MenuItem(gt(i), i.friendly_name, i.description) for i in handlers]


def get_menuitems_text(menuitems, pred=lambda x: True):
    """
    Returns a list of 'friendly_name's from the list of menuitems generated
    with `get_menuitems_for_handlers`, filtered by the given `pred`icate
    (defaults to all items).
    """
    return [i.t for i in menuitems if pred(i) is True]


def get_choice_index(menuitems, choice):
    """
    Return the index of the menu item for the given friendly_name
    """
    try:
        return [i.v for i in menuitems].index(choice)
    except Exception:
        return 0


def get_value_by_text(menuitems, name):
    """Return the value (source/output_type) for the given friendly_name."""
    try:
        return [i.v for i in menuitems if i.t == name][0]
    except IndexError:
        return None


def get_text_by_value(menuitems, choice):
    """Takes the choice of the menu and returns the name to print"""
    try:
        return [i.t for i in menuitems if i.v == choice][0]
    except IndexError:
        return None


def get_description_by_text(menuitems):
    def previewer(choice):
        try:
            desc = [i.d for i in menuitems if i.t == choice]
            return fmt.format(desc[0])
        except Exception:
            pass
    return previewer


class run_cleaner:
    # pass

    def __init__(self, settings):
        self.it = 0
        self.settings = settings
        self.count = len(settings.sources)
        self.source_name = ''

    def __call__(self):
        try:    # with this logic the last call goes out of range, so this.
            self.source_name = highlight(self.settings.sources[self.it])
            self.it += 1
        except Exception:
            pass

        pre_menu(
            self.settings,
            (f"Please Wait, I'm working on {self.source_name}"
             f" ({self.it}/{self.count})")
        )

        return (self.it, self.source_name)


class formatter(string.Formatter):
    """ Custom formatter to use our syntax highlight formatting style for
    descriptions."""
    def get_colored_style(self, spec):
        c, s = spec, None
        try:
            c, s = spec.split("|")
            s = s.split(",")
        except Exception:
            pass
        # assuming correct colors are given, if _col_ is not in colors
        # we assume it's one (or list of) styling, especially if none are given
        if c not in COLORS.keys() and not s:
            s = c.split(',')
            c = None
        return (c, s)

    def get_value(self, key, args, kwargs):
        return key

    def format_field(self, value, format_spec=[]):
        col, style = self.get_colored_style(format_spec)
        value = colored(value, color=col, attrs=style)
        return super(formatter, self).format(value, format_spec)


fmt = formatter()
