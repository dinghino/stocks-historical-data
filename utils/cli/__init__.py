from termcolor import colored
from utils.cli.formatter import formatter as _formatter


format = _formatter().format


def highlight(text, color='cyan', attrs=['bold']):
    return colored(text, color, attrs=attrs)
