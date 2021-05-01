import click
from termcolor import colored
from simple_term_menu import TerminalMenu


BACK_TXT = '[ BACK ]'


def get_choices(menu_items):
    return [item[0] for item in menu_items]


def handle_choice(menu_items, choice, settings):
    return menu_items[choice][1](settings)


def run_menu(menu_items, settings, header=None, description=None):

    menu_exit = False
    menu = TerminalMenu(get_choices(menu_items))

    while not menu_exit:
        pre_menu(settings, header, description)

        choice = menu.show()
        menu_exit = handle_choice(menu_items, choice, settings)


def handle_go_back(settings):
    return True


def print_current_options(settings):
    click.echo(colored("Current Options", "cyan", attrs=['bold']))
    items = settings.serialize()
    del items['settings_path']  # for now at least we don't want to show this

    for k, v in items.items():
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
        except settings.DateException:
            message = highlight('\nInvalid format.', 'red')
            message += 'Should be one of '
            formats = get_date_format_str(settings)
            click.echo(highlight(message, 'red') + formats + '\n')
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
