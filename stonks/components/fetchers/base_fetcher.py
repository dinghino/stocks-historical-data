import abc
from datetime import datetime, timedelta
from contextlib import closing
import requests
import click

from stonks.components.component_base import ComponentBase

# Click progressbar settings for the main request loop
PROGRESS_SETTINGS = {
    "label": "Processing",
    "fill_char": "█",
    "show_pos": True,
    "show_percent": True,
}


class Fetcher(ComponentBase):
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.tickers = settings.tickers or []
        self.start_date = settings.start_date or datetime(2019, 1, 1).date()
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
    def make_url(self, *args, **kwargs):  # pragma: no cover
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
        if self.loop_tickers_not_dates:
            return len(self.settings.tickers)
        return len(list(self.date_range()))

    def get_urls_loop(self):
        if self.loop_tickers_not_dates:
            return self.tickers_range
        return self.date_range

    def make_requests(self, *args, **kwargs):
        """Actually perform the requests. Generate the urls with `make_url`,
        provided by the child classes. optional arguments can be passed through
        the `run` method (ideally from the main app object that should know
        what fetcher has created."""
        main_loop = self.get_urls_loop()

        for url_source in main_loop():
            for url in self.make_url(url_source, *args, **kwargs):
                # If the url is already been processed skip it
                if not self.validate_new_url(url):  # pragma: no cover
                    continue

                with closing(requests.get(url, stream=True)) as response:
                    if not response or not response.ok:
                        continue

                    yield response

    def run(self, show_progress=False, tickers=None, *args, **kwargs):
        self._done = False

        if show_progress:  # pragma: no cover
            length = self.get_iter_count()
            with click.progressbar(length=length, **PROGRESS_SETTINGS) as bar:
                for response in self.make_requests(*args, **kwargs):
                    yield response
                    bar.update(1)
        else:
            for response in self.make_requests(*args, **kwargs):
                yield response

        self.done()
