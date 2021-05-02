import os
import click
from cli import entry
from stonks import Settings


def start():
    os.system('clear')

    settings = Settings()
    if settings.init():
        click.echo("Settings loaded")
    else:
        click.echo("There was an error Loading the settings")

    entry.run(settings)


if __name__ == "__main__":
    from stonks.components import writers, handlers
    from cli.setup import setup

    dialects = [("default", {"delimiter": "|"})]

    setup(handlers, writers, dialects)
    start()
