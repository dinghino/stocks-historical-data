import os

import click
import utils
from cli import helpers
from stonks import manager


def validate_settings(settings, echo=True):
    if helpers.validate_settings(settings, False):
        return True
    utils.cli.echo_divider()
    msg = "\nRun aborted. There are missing required settings.\n"
    click.echo(utils.cli.highlight(msg, 'red'))
    click.pause()
    return False


def handle_processing(result, curr, total, echo=True):
    if not echo:
        return
    source = manager.get_source_friendly_name(result.source)

    source = utils.cli.highlight(source)
    msg = f"Please wait. Working on {source} ({curr}/{total})\n"
    click.echo(utils.cli.highlight(msg, 'yellow'))


def add_result(results, type, msg):
    results.append({'type': type, 'message': msg})


def get_results(results, type):
    return [r['message'] for r in results if r['type'] == type]


def prep_result(result, color):
    source = manager.get_source_friendly_name(result.source)
    tickers = result.tickers
    if len(tickers) > 5:
        tickers = [*tickers[0:4], "..."]
    tickers = ', '.join(tickers)
    return utils.cli.highlight(f'{source} for {tickers}', color)


def handle_error(result, results):
    err = prep_result(result, 'red')
    if result.message:
        err = err + ' - ' + utils.cli.highlight(result.message, 'red')
    add_result(results, 'error', err)


def handle_done(result, results):
    msg = prep_result(result, 'green')
    if result.message:
        msg = msg + ' - ' + result.message
    add_result(results, 'success', msg)


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
    if not clear_screen:
        utils.cli.echo_divider()
        click.echo()
    click.echo(completed_msg)
    click.echo()
    texts, space = format_results(results)
    for (msg, fname) in texts:
        click.echo(f'- {msg:<{space+2}} {fname}')
    utils.cli.echo_divider()
    done and click.echo(path_location)


def format_results(results):
    ps = [(o[0], o[1]) for o in (r['message'].split(' - ') for r in results)]
    ml = max(len(i[0]) for i in ps)
    return ps, ml
