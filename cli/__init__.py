import os
import click
from cli import entry
import stonks


def launch():
    if not stonks.init():
        return echo_error()

    os.system('clear')
    settings = stonks.Settings()
    if settings.init():
        click.echo("Settings loaded")
        entry.run(settings)
    else:
        click.echo("There was an error Loading the settings")


def echo_error():
    click.echo(click.style(
        "There was an error in setup. Sorry! Why? Who knows!"))
