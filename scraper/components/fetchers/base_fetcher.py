import abc
import codecs, csv
from datetime import datetime, timedelta
from contextlib import closing
import requests
import click
from scraper import utils


class Fetcher(abc.ABC):
    def __init__(self, settings, debug=False):
        self.tickers = settings.tickers or []
        self.start_date = settings.start_date or dt(2020,5,1).date()
        self.end_date = settings.end_date or datetime.now().date()

        self._debug = debug
        self._done = False

    # @abc.abstractmethod
    def daterange(self):
        """Generate the date iterator to loop all the data to fetch"""
        for n in range(int((self.end_date - self.start_date).days)):
            yield self.start_date + timedelta(n)

    def done(self):
        self._done = True

    def process_file_to_csv(self, response):
        """
        Takes the raw output from the response and outputs a csv readable stream
        """
        return codecs.iterdecode(response.iter_lines(), 'utf-8')

    @abc.abstractmethod
    def make_url(self, date):
        raise NotImplementedError

    def run(self, show_progress=True, *args, **kwargs):
        self._done = False
        if show_progress:
            i = 0   # used for progress_bar
            dates_count = len(list(self.daterange()))
            utils.progress_bar(0, dates_count, length = 50)

        for date in self.daterange():
            for url in self.make_url(date):
                if not url: continue

                with closing(requests.get(url, stream=True)) as response:
                    if response.status_code == 200:
                        yield response

            if show_progress:
                utils.progress_bar(i + 1, dates_count, length = 50)
                i += 1

        self.done()
