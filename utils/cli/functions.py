import shutil

import click
from termcolor import colored


def highlight(text, color='cyan', attrs=['bold']):
    return colored(text, color, attrs=attrs)


def get_terminal_size(fallback=(80, 20)):
    return shutil.get_terminal_size(fallback)


def terminal_width():
    w, _ = get_terminal_size()
    return w


def echo_divider():
    click.echo('\n' + '-' * terminal_width() + '\n')
