import os
from pathlib import Path
import shutil   # noqa

import click
# from termcolor import colored
from simple_term_menu import TerminalMenu
from cli import utils


def description():
    disclaimer = utils.highlight(
        '\nFeature not fully implemented - READ ONLY', 'red')

    return ("Navigate your file system, find and preview your data.\n"
            "You can select an existing output file to automatically detect\n"
            "settings and continue on that file.\n"
            f"{disclaimer}" "\n")


def run(settings):
    done = False
    viewer = get_file_viewer(False)

    path = os.path.abspath(settings.output_path)

    if not path:
        path = get_root()

    while not done:
        utils.pre_menu(
            settings, "Navigate and preview your files", description())

        # terminal-menu formats the string with the file name. this produces
        # the required command, appending first the full path to cwd + '/{}'
        preview_command = viewer(path)

        fields = list_files(path)
        BACK = "[x] " + utils.BACK_TXT
        menu = TerminalMenu(
            (BACK, '..',  *fields),
            preview_command=preview_command)

        menu.show()

        choice = menu.chosen_menu_entry

        full_path = os.path.join(path, choice)
        if choice == '..':
            path = get_parent(path)
        elif choice == utils.BACK_TXT:
            done = True
        elif not is_file(full_path):
            path = os.path.join(path, choice)
            pass
        else:  # File found, do something!
            click.echo(utils.highlight("File Selected!", 'green'))
            click.echo("Something will be done in the future!")
            done = True
            click.pause()


def is_file(path):
    return os.path.isfile(path)


def get_parent(path):
    return Path(path).parent


def get_root():
    """ Returns the root of the project.
    In the future it should/could return the $HOME directory
    """
    # return get_parent(os.path.dirname(os.path.abspath(__file__)))
    return os.path.abspath(Path.home())


def get_file_viewer(use_head=True):

    call_bat = "bat -p --color=always {}/{}"
    call_cat = "cat {}/{}"
    head = "head -10 {}/{}"

    if use_head:
        viewer = head
    elif shutil.which('bat'):
        viewer = call_bat
    else:
        viewer = call_cat

    def function(path):
        return viewer.format(path, '{}')  # allows for further formatting
    return function


def list_files(directory):
    return (
        file for file in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, file)) or
        file.endswith('.csv') or file.endswith('.txt')
        # if os.path.isfile(os.path.join(directory, file))
        # and not (file.endswith('.zip') or file.endswith('.xml'))
    )


# =============================================================================

# Custom visualizer from simple-term-menu examples at
# https://pypi.org/project/simple-term-menu/
# TODO: Implement to be agnostic of operating system or
# def highlight_file(filepath):
#     # TODO: add to requirements.txt if used
#     from pygments import formatters, highlight, lexers
#     from pygments.util import ClassNotFound

#     with open(filepath, "r") as f:
#         file_content = f.read()
#     try:
#         lexer = lexers.get_lexer_for_filename(
#             filepath, stripnl=False, stripall=False)
#     except ClassNotFound:
        # lexer = lexers.get_lexer_by_name("text", stripnl=False, stripall=False) # noqa
#     formatter = formatters.TerminalFormatter(bg="dark")  # dark or light
#     highlighted_file_content = highlight(file_content, lexer, formatter)
#     return highlighted_file_content
