import click
from launcher import validators
import cli as stonks_cli


@click.group(invoke_without_command=True)
@click.option('-s', '--settings', callback=validators.settings_path,
              help="Path to a settings file to load")
@click.pass_context
def main(ctx, settings):
    print("Hello world from main")


@main.command()
@click.pass_context
def test(ctx, *args, **kwargs):
    print("Hello world from test")
    print(ctx.obj)
    print(args)
    print(kwargs)


@main.command()
@click.pass_context
def cli(ctx, settings=None):
    click.echo(ctx)
    click.pause()
    stonks_cli.launch(settings)


def launch_custom(path):
    pass
