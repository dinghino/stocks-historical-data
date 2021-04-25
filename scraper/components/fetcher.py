import os
import codecs
import csv
from datetime import datetime as dt, timedelta
import requests
from contextlib import closing

URL_BASE = "http://regsho.finra.org/CNMSshvol"
URL_END = ".txt"

class Fetcher:

    def __init__(self,
        parser,
        tickers = [],
        start_date = dt(2020,5,1).date(),
        end_date=dt.now().date(), debug=False):

        # if parser is None:
        #     raise ParserMissingException

        self.parser = parser
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date

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
        
        # self.__debug_get_data(date, url)

        with closing(requests.get(url, stream=True)) as r:
            reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
            # store the header row for the csv
            self.parser.cache_header(next(reader))
            # yield the rows for processing
            for row in reader:
                yield row

    def run(self, tickers = []):
        self.__debug_run()
        i = 0
        dates_count = len(list(self._daterange()))
        printProgressBar(0, dates_count, prefix = 'Downloading:', suffix = 'Complete', length = 50)
        for date in self._daterange():
            for row in self.get_data(date):
                self.parser.parse(row, self.tickers)
            printProgressBar(i + 1, dates_count, prefix = 'Downloading:', suffix = 'Complete', length = 50)
            i = i+1


    def __debug_run(self):
        if self._debug is True:
            print("fetching data for {}, from {} to {}\n".format(
                ','.join(self.tickers),
                self.start_date,
                self.end_date))

    def __debug_get_data(self, date, url):
        if self._debug is True:
            print("fetching data for {} from {}".format(date.strftime("%Y-%m-%d"), url))


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# Exceptions ==================================================================

# class ParserMissingException(Exception):
#     print("Fetcher needs a parser!")
# class TickerMissingException(Exception):
#     print("Fetcher needs a list of tickers to parse")

# class SourceException(Exception):
#     """Source should be included in available sources"""
#     print("Fetcher source data should be one of {}".format(', '.join(Fetcher._sources)))
#     pass 

# class SourceNotAvailable(Exception):
#     print("Selected source is currently not processable")
#     pass
