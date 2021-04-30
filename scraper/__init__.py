import os

from scraper.settings import Settings
from scraper.stocks import App
from scraper import components
from scraper import utils


from scraper.components import fetchers, parsers, manager, writers
from scraper.settings.constants import SOURCES, OUTPUT_TYPE

manager.register_handler(SOURCES.FINRA_SHORTS, fetchers.Finra, parsers.Finra)
manager.register_handler(SOURCES.SEC_FTD, fetchers.SecFtd, parsers.SecFtd)
manager.register_writer(OUTPUT_TYPE.SINGLE_FILE, writers.SingleFile)
manager.register_writer(OUTPUT_TYPE.SINGLE_TICKER, writers.MultiFile)

# Root dir for scraper
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

