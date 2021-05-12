import click
import utils
from stonks.components import manager

from cli.helpers.handlers import HandlersMenuItems


def noop(): return click.pause()


def is_list(o):
    return type(o) is list


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
            utils.cli.highlight(v, None, attrs=['bold'])
            ))
