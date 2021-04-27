from scraper.components.fetchers.base_fetcher import Fetcher
# import scraper.utils as utils

class NasdaqFetcher(Fetcher):

    URL = "https://api.nasdaq.com/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit={limit}&todate={end}"

    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def make_url(self, ticker, *args, **kwargs):
        """ Get the url for the specified date for the given source"""
        def tostr(d):
            return d.strftime("%Y-%m-%d")

        start_ = self.start_date
        end_ = self.end_date
        # timedelta object -> number of days
        limit = (end_ - start_).days

        # return self.URL_BASE + str(date) + self.URL_END
        yield self.URL.format(start=tostr(start_), end=tostr(end_), limit=limit, ticker=ticker)
