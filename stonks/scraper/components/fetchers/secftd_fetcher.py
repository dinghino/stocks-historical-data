from scraper.settings.constants import SOURCES
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

    @staticmethod
    def is_for():
        return SOURCES.SEC_FTD

    def make_url(self, date, *args, **kwargs):
        date = date.strftime("%Y%m")

        for v in self.URL_VARIANTS:
            url = self.URL_BASE + str(date) + v + self.URL_END
            # Since we receive ALL days from our caller and in this case we
            # work on a monthly basis, we check if the url has already been
            # processed and if so sky to the next one until we reach new month

            yield url
