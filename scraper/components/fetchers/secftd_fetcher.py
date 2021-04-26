from scraper.components.fetchers.base_fetcher import Fetcher
# from dateutil.relativedelta import relativedelta

# Url sample
# https://www.sec.gov/files/data/fails-deliver-data/cnsfails202103b.zip
# split into
# - BASE: https://www.sec.gov/files/data/fails-deliver-data/cnsfails
# - dateformat %Y%m
# - [a/b] (both, they indicate first and second half o the year)
#  - END .zip

class SecFtdFetcher(Fetcher):

    URL_BASE = "https://www.sec.gov/files/data/fails-deliver-data/cnsfails"
    URL_VARIANTS = ["a", "b"]
    URL_END = ".zip"

    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)
        self.processed = []
    
    def done(self):
        super().done()
        self.processed = []

    def make_url(self, date, *args, **kwargs):
        date = date.strftime("%Y%m")

        for v in self.URL_VARIANTS:
            url = self.URL_BASE + str(date) + v + self.URL_END
            # Since we receive ALL days from our caller and in this case we work
            # on a monthly basis, we check if the url has already been processed
            # and if so sky to the next one until we reach a new month
            if url in self.processed:
                continue

            self.processed.append(url)
            yield url
