import os
from cli import entry
from stonks import Settings
from stonks.components import fetchers, parsers, manager, writers
from stonks.constants import SOURCES, OUTPUT_TYPE

# Settings object for the whole app


def start():
    # register default components for the app
    manager.register_handler(
        SOURCES.FINRA_SHORTS, fetchers.Finra, parsers.Finra)
    manager.register_handler(
        SOURCES.SEC_FTD, fetchers.SecFtd, parsers.SecFtd)
    manager.register_writer(
        OUTPUT_TYPE.SINGLE_FILE, writers.SingleFile)
    manager.register_writer(
        OUTPUT_TYPE.SINGLE_TICKER, writers.MultiFile)

    manager.register_dialect('default', delimiter='|')

    settings = Settings()

    os.system('clear')

    if settings.init():
        print("Settings loaded")
    else:
        print("There was an error Loading the settings")

    entry.run(settings)


if __name__ == "__main__":
    start()
