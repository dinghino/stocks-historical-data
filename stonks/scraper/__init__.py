import os

from scraper.settings import Settings   # noqa
from scraper.stocks import App          # noqa
from scraper import components          # noqa
from scraper import utils               # noqa

# Root dir for scraper
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
