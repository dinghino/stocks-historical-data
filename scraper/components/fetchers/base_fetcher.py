import abc
import codecs, csv
from datetime import datetime, timedelta
from contextlib import closing
import requests

from scraper import utils


class Fetcher(abc.ABC):
    def __init__(self, settings, debug=False):
        self.tickers = settings.tickers or []
        self.start_date = settings.start_date or dt(2020,5,1).date()
        self.end_date = settings.end_date or datetime.now().date()

        self._debug = debug


    def _daterange(self):
        """Generate the date iterator to loop all the data to fetch"""
        for n in range(int((self.end_date - self.start_date).days)):
            yield self.start_date + timedelta(n)

    @abc.abstractmethod
    def make_url(self, date, *args, **kwargs):
        raise NotImplementedError
    
    def get_data(self, date, *args, **kwargs):
        url = self.make_url(date, args, kwargs)
        
        with closing(requests.get(url, stream=True)) as r:
            reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
            # yield the rows for processing
            for row in reader:
                yield row

    def run(self, *args, **kwargs):

        i = 0   # used for progress_bar
        dates_count = len(list(self._daterange()))
        utils.progress_bar(0, dates_count, prefix = 'Downloading:', suffix = 'Complete', length = 50)
        for date in self._daterange():
            for row in self.get_data(date, args, kwargs):
                yield row
            utils.progress_bar(i + 1, dates_count, prefix = 'Downloading:', suffix = 'Complete', length = 50)
            i = i+1
