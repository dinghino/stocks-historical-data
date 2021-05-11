import json
import click
import utils


def settings_path(allow_empty=False):
    def validator_function(ctx, settings):
        if not settings:
            return False
        path = utils.path.parse(settings)
        try:
            with open(path) as file:
                json.loads(file.read())
        except FileNotFoundError:
            click.echo(f"Could not find settings at {path}")
            if not allow_empty:
                ctx.abort()
            click.echo("Generating new settings file on save")
        except json.JSONDecodeError:
            click.echo('File is wrongly formatted.')
            ctx.abort()
        return path
    return validator_function
