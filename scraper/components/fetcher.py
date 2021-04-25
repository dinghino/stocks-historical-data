import os
import codecs
import csv
from datetime import datetime as dt, timedelta
import requests
from contextlib import closing

from scraper import Settings, utils
# import scraper.utils as utils

URL_BASE = "http://regsho.finra.org/CNMSshvol"
URL_END = ".txt"

class Fetcher:

    def __init__(self, parser, settings, debug=False):

        self.parser = parser

        self.tickers = settings.tickers or []
        self.start_date = settings.start_date or dt(2020,5,1).date()
        self.end_date = settings.end_date or dt.now().date()

        self._debug = debug

    @property
    def data(self):
        return self.parser.data

    def _make_url(self, date):
        """ Get the url for the specified date for the given source"""
        date = date.strftime("%Y%m%d")
        return URL_BASE + str(date) + URL_END

    def _daterange(self):
        """Generate the date iterator to loop all the data to fetch"""
        for n in range(int((self.end_date - self.start_date).days)):
            yield self.start_date + timedelta(n)

    def get_data(self, date):
        url = self._make_url(date)
        
        with closing(requests.get(url, stream=True)) as r:
            reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
            # store the header row for the csv
            self.parser.cache_header(next(reader))
            # yield the rows for processing
            for row in reader:
                yield row

    def run(self, tickers = []):

        i = 0   # used for progress_bar
        dates_count = len(list(self._daterange()))
        utils.progress_bar(0, dates_count, prefix = 'Downloading:', suffix = 'Complete', length = 50)
        for date in self._daterange():
            for row in self.get_data(date):
                self.parser.parse(row, self.tickers)
            utils.progress_bar(i + 1, dates_count, prefix = 'Downloading:', suffix = 'Complete', length = 50)
            i = i+1
