from scraper.components.fetchers.base_fetcher import Fetcher
# import scraper.utils as utils

class FinraFetcher(Fetcher):

    URL_BASE = "http://regsho.finra.org/CNMSshvol"
    URL_END = ".txt"

    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def make_url(self, date, *args, **kwargs):
        """ Get the url for the specified date for the given source"""
        date = date.strftime("%Y%m%d")
        # return self.URL_BASE + str(date) + self.URL_END
        url = "{}{}{}".format(self.URL_BASE, date, self.URL_END)
        
        yield url
