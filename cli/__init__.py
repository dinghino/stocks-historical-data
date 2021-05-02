import os
import click
from cli import entry
from stonks import Settings
from stonks.components import manager, writers, handlers


def launch():
    if init():
        start()
    else:
        echo_error()


def init(handlers_module=None, writers_module=None, dialects=[]):
    done = True
    dialects = [('default', {'delimiter': '|'}), *dialects]
    # register native components
    done = done and manager.register_dialects_from_list(dialects)
    done = done and manager.register_writers_from_module(writers)
    done = done and manager.register_handlers_from_modules(handlers)

    # process extra components provided on setup
    if handlers_module:
        done = done and manager.register_handlers_from_modules(handlers_module)
    if writers_module:
        done = done and manager.register_writers_from_module(writers_module)

    return done


def start():
    os.system('clear')

    settings = Settings()
    if settings.init():
        click.echo("Settings loaded")
    else:
        click.echo("There was an error Loading the settings")

    entry.run(settings)


def echo_error():
    click.echo(click.style(
        "There was an error in setup. Sorry! Why? Who knows!"))
