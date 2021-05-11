import click
import utils
from cli.helpers import functions as funcs


class Page:
    def __init__(self, header=None, description=None, handler=funcs.noop):
        self.header = None
        self.description = None

        if header:
            self.header = utils.cli.format(header)
        if description:
            self.description = utils.cli.format(description)

        self.page_handler = handler

    def print_settings(self, settings):
        funcs.print_current_options(settings)

    def pre_menu(self, settings):
        click.clear()
        self.print_settings(settings)

        click.echo()
        if (self.header):
            click.echo(
                utils.cli.highlight(self.header, 'yellow', attrs=['bold']))
            click.echo()
        if self.description:
            click.echo(self.description)
            click.echo()

        funcs.validate_settings(settings)

    def __call__(self, settings):
        self.pre_menu(settings)
        return self.page_handler(settings)
