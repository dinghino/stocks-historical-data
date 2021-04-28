from scraper.settings import Settings
from scraper.stocks import App
from scraper import components
from scraper import utils


from scraper.components import fetchers, parsers, manager
from scraper.settings.constants import SOURCES

manager.register(SOURCES.FINRA_SHORTS, fetchers.Finra, parsers.Finra)
manager.register(SOURCES.SEC_FTD, fetchers.SecFtd, parsers.SecFtd)
