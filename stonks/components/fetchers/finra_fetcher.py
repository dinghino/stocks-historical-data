from stonks.constants import SOURCES
from stonks.components.base_fetcher import Fetcher


class FinraFetcher(Fetcher):

    URL_BASE = "http://regsho.finra.org/CNMSshvol"
    URL_END = ".txt"

    @staticmethod
    def is_for():
        return SOURCES.FINRA_SHORTS

    def make_url(self, date, *args, **kwargs):
        """ Get the url for the specified date for the given source"""
        date = date.strftime("%Y%m%d")
        # return self.URL_BASE + str(date) + self.URL_END
        url = "{}{}{}".format(self.URL_BASE, date, self.URL_END)

        yield url
