import os

import click
import utils
from cli import helpers


def validate_settings(settings, echo=True):
    if helpers.validate_settings(settings, False):
        return True
    utils.cli.echo_divider()
    msg = "\nRun aborted. There are missing required settings.\n"
    click.echo(utils.cli.highlight(msg, 'red'))
    click.pause()
    return False


def handle_processing(source, curr, total, echo=True):
    if not echo:
        return

    source = utils.cli.highlight(source)
    msg = f"Please wait. Working on {source} ({curr}/{total})\n"
    click.echo(utils.cli.highlight(msg, 'yellow'))


def add_result(results, type, msg):
    results.append({'type': type, 'message': msg})


def get_results(results, type):
    return [r['message'] for r in results if r['type'] == type]


def handle_error(source, results):
    err = utils.cli.highlight(f"{source} had processing errors.", "red")
    add_result(results, 'error', err)


def handle_done(source, results):
    res = utils.cli.highlight(f'{source} succesfully processed.', 'green')
    add_result(results, 'success', res)


def print_outcome(settings, results, echo=True, clear_screen=True):
    if not echo:
        return

    out_folder = utils.cli.highlight(os.path.abspath(settings.output_path))
    path_location = f"You can find your data in\n{out_folder}"

    done = True
    errors = get_results(results, 'error')

    if len(errors) == 0:
        completed_msg = utils.cli.highlight('All Done!', 'green')
    elif 0 < len(errors) < len(settings.sources):
        completed_msg = utils.cli.highlight('Completed with errors', 'yellow')
    else:
        done = False
        completed_msg = utils.cli.highlight("Could not get your data", 'red')

    clear_screen and click.clear()
    click.echo(completed_msg)
    click.echo('\n'.join(['- ' + r['message'] for r in results]))
    utils.cli.echo_divider()
    done and click.echo(path_location)


def _echo(e=True, *args, **kwargs):
    e and click.echo(*args, **kwargs)
