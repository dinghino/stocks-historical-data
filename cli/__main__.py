import cli
import click


if __name__ == "__main__":

    if cli.setup():
        cli.start()
    else:
        click.echo(
            click.style("There was an error in setup. Sorry! Why? Who knows!",
                        fg="red")
            )
