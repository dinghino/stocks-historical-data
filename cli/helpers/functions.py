import click
from termcolor import colored

from stonks import manager
import utils

from cli.helpers.handlers import HandlersMenuItems


def noop(): return click.pause()


def is_list(o):
    return type(o) is list


# NOTE: This is still used in the launchers. Might want to remove it
def print_current_options(settings):
    click.echo(utils.cli.highlight("Current Options"))
    items = settings.serialize()
    # for now at least we don't want to show this
    del items['settings_path']

    # Get the handlers from the manager to match the settings value with
    # the proper connected text
    mi_sh = HandlersMenuItems(manager.get_all_handlers())
    mi_wh = HandlersMenuItems(manager.get_all_writers())

    for k, v in items.items():
        if k == 'Type':
            v = mi_wh.get_name_by_value(v)
        elif k == 'Sources' and type(v) is list:
            v = [mi_sh.get_name_by_value(x) for x in v]
        if type(v) is list:  # beautify lists
            v = ', '.join(v)

        click.echo("{}\t{}".format(
            utils.cli.highlight(k),
            utils.cli.highlight(v, None, attrs=['bold']))
            )


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
