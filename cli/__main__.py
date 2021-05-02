from cli import cli
from cli.setup import setup
from stonks.components import writers, handlers

# ===========================================================================

if __name__ == "__main__":

    dialects = [("default", {"delimiter": "|"})]
    setup(handlers, writers, dialects)

    cli.start()
