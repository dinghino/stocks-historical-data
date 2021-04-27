import abc
import codecs, csv
from datetime import datetime, timedelta
from contextlib import closing
import requests
import click
from scraper import utils


class Fetcher(abc.ABC):
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.tickers = settings.tickers or []
        self.start_date = settings.start_date or dt(2019,1,1).date()
        self.end_date = settings.end_date or datetime.now().date()

        self._debug = debug
        self._done = False

        self.processed = []
        # TODO: Implement the option to change it. This is needed to loop
        # the tickers when the fetcherss that work on ticker and not on date
        # loops (i.e. nasdaq) need to grab stuff.
        self.loop_tickers_not_dates = False

    # @abc.abstractmethod
    def date_range(self):
        """Generate the date iterator to loop all the data to fetch"""
        for n in range(int((self.end_date - self.start_date).days)):
            yield self.start_date + timedelta(n)

    def done(self):
        self._done = True
        self.processed = []

    @abc.abstractmethod
    def make_url(self, *args, **kwargs):
        raise NotImplementedError

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

    def make_requests(self, *args, **kwargs):
        # NOTE: make_url methods MUST take the first (and only?) argument as
        # the one they use to create the actual url, either the "current date".
        # or "current ticker" that's being processed
        # If in the future this breaks for some reason (i.e. a fetcher needs
        # more info from a loop) we can revert to looping the dates and moving
        # specific loops inside the make_url methods (i.e. nasdaq.make_url will
        # loop the tickers from settings to generate them).
        # This would be less efficient but would work just fine.
        main_loop = self.tickers_range if self.loop_tickers_not_dates else self.date_range

        for url_source in main_loop():
            for url in self.make_url(url_source, *args, **kwargs):
                # If the url is already been processed skip it
                if not self.validate_new_url(url):
                    continue


                with closing(requests.get(url)) as response:
                    if response.status_code == 200:
                        yield response
                    yield None

    def run(self, show_progress=True, tickers=None, *args, **kwargs):
        self._done = False
        max_progr = self.get_progress_max_value()
        progress = self.progress_bar(show_progress, -1, max_progr)

        for response in self.make_requests(*args, **kwargs):
            if not response:
                progress = self.progress_bar(show_progress, progress, max_progr)
                continue

            yield response
            progress = self.progress_bar(show_progress, progress, max_progr)

        self.done()

    def progress_bar(self, show_progress, curr, max):
        curr +=1
        if show_progress:
            utils.progress_bar(curr, max, length = 50)
        return curr

    def get_progress_max_value(self):
        if self.loop_tickers_not_dates:
            return len(self.settings.tickers)
        return len(list(self.date_range()))
