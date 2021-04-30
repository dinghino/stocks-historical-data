import abc
import codecs, csv
from datetime import datetime, timedelta
from contextlib import closing
import requests
import click

from scraper.components.component_base import ComponentBase
from scraper import utils

# Click progressbar settings for the main request loop
PROGRESS_BAR_SETTINGS = {
    "label":"Processing",
    "fill_char":"█",
    "show_pos":True,
    "show_percent":True,
}

class Fetcher(ComponentBase):
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.tickers = settings.tickers or []
        self.start_date = settings.start_date or datetime(2019,1,1).date()
        self.end_date = settings.end_date or datetime.now().date()

        self._debug = debug
        self._done = False

        self.processed = []
        # TODO: Implement the option to change it. This is needed to loop
        # the tickers when the fetcherss that work on ticker and not on date
        # loops (i.e. nasdaq) need to grab stuff.
        self.loop_tickers_not_dates = False

        # progress bar settings
        self._prgrs = -1
        self._prgrs_max = 0
        self._show_progress = False

    # @abc.abstractmethod
    def date_range(self):
        """Generate the date iterator to loop all the data to fetch"""

        if self.start_date == self.end_date:
            yield self.start_date
        else:
            for n in range(int((self.end_date - self.start_date).days)):
                yield self.start_date + timedelta(n)

    def done(self):
        self._done = True
        self.processed = []

    @abc.abstractmethod
    def make_url(self, *args, **kwargs): # pragma: no cover
        return NotImplemented

    # if the provided url is in the processed list return None, otherwise
    # add it and return it.
    def validate_new_url(self, url):
        if url in self.processed:
            return None
        self.processed.append(url)
        return url

    def tickers_range(self):
        for ticker in self.settings.tickers:
            yield ticker

    def get_iter_count(self):
        return len(self.settings.tickers) if self.loop_tickers_not_dates else len(list(self.date_range()))

    def get_urls_loop(self):
        return self.tickers_range if self.loop_tickers_not_dates else self.date_range

    def make_requests(self, *args, **kwargs):
        # NOTE: make_url methods MUST take the first (and only?) argument as
        # the one they use to create the actual url, either the "current date".
        # or "current ticker" that's being processed
        # If in the future this breaks for some reason (i.e. a fetcher needs
        # more info from a loop) we can revert to looping the dates and moving
        # specific loops inside the make_url methods (i.e. nasdaq.make_url will
        # loop the tickers from settings to generate them).
        # This would be less efficient but would work just fine.
        main_loop = self.get_urls_loop()
        count = self.get_iter_count()

        with click.progressbar(length=count, **PROGRESS_BAR_SETTINGS) as bar:
            for url_source in main_loop():
                for url in self.make_url(url_source, *args, **kwargs):
                    # If the url is already been processed skip it
                    if not self.validate_new_url(url): # pragma: no cover
                        yield None
                        continue

                    with closing(requests.get(url, stream=True)) as response:
                        yield response
                bar.update(1)

    def run(self, show_progress=True, tickers=None, *args, **kwargs):
        self._done = False
        self._show_progress = show_progress

        for response in self.make_requests(*args, **kwargs):
            if not response or not response.status_code == 200:
                continue

            yield response

        self.done()
