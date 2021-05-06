import json
import click
from launcher import utils


def settings_path(ctx, settings):
    if not settings:
        return False
    path = utils.parse_path(settings)
    try:
        with open(path) as file:
            json.loads(file.read())
    except FileNotFoundError:
        click.echo(f"Could not find settings at {path}")
        ctx.abort()
    except json.JSONDecodeError:
        click.echo('File is wrongly formatted.')
        ctx.abort()
    return path
