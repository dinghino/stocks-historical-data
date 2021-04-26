from scraper.components.fetchers.base_fetcher import Fetcher
# import scraper.utils as utils

URL_BASE = "http://regsho.finra.org/CNMSshvol"
URL_END = ".txt"

class FinraFetcher(Fetcher):

    URL_BASE = "http://regsho.finra.org/CNMSshvol"
    URL_END = ".txt"

    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def make_url(self, date):
        """ Get the url for the specified date for the given source"""
        date = date.strftime("%Y%m%d")
        return self.URL_BASE + str(date) + self.URL_END
