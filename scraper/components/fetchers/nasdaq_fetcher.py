from scraper.settings.constants import SOURCES
from scraper.components.fetchers.base_fetcher import Fetcher
# import scraper.utils as utils

class NasdaqFetcher(Fetcher):

    URL = "https://api.nasdaq.com/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit={limit}&todate={end}"

    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)
        self.loop_tickers_not_dates = True

    @staticmethod
    def is_for():
        # TODO: Actually write its component and constants
        return "NASDAQ"

    def make_url(self, ticker, *args, **kwargs):
        """ Get the url for the specified date for the given source """
        
        # if ticker not in self.settings.tickers:
        #     raise ValueError(f'NasdaqFetcher: where does ticker '{ticker}' comes from?')

        def tostr(d):
            """ Format the date in nasdaq url format type """
            return d.strftime("%Y-%m-%d")

        start_ = self.start_date
        end_ = self.end_date
        # timedelta object -> number of days
        limit = (end_ - start_).days

        url = self.URL.format(start=tostr(start_), end=tostr(end_), limit=limit, ticker=ticker)

        yield url

