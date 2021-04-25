# from datetime import datetime as dt
import os
import datetime

from scraper.settings import Settings
from scraper.components import Fetcher
from scraper.components import FinraParser
from scraper.components import SingleTickerWriter, SingleFileWriter



class StockScraper:

    def __init__(self, settings, debug=False):
        
        self.settings = settings
        self._debug = debug

        self._strip_ticker_when_parsing = self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_FILE

        if self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_FILE:
            self._WriterClass = SingleFileWriter
        elif self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_TICKER:
            self._WriterClass = SingleTickerWriter
        else:
            raise Exception("There was an error setting up the file writer!")

    def run(self):

        # if self.settings.start_date is None:
        #     self.settings.start_date = "2020-5-1"
        # if self.settings.end_date is None:
        #     self.settings.end_date = datetime.datetime.now().date()

        self.writer = self._WriterClass(self.settings.output_path)
        self.parser = FinraParser(strip_ticker=self._strip_ticker_when_parsing)

        self.fetcher = Fetcher(
            parser=self.parser,
            tickers=self.settings.tickers,
            start_date=self.settings.start_date,
            end_date=self.settings.end_date,
            debug=self._debug
        )

        os.system("clear")
        print("Start Date set to {}".format(self.start_date.strftime('%Y-%m-%d')))
        print("Start Date set to {}".format(self.start_date.strftime('%Y-%m-%d')))
        print("\n")
        print("Pulling data for")
        print(' '.join(self.settings.tickers))
        print("\n")

        self.fetcher.run()
        self.writer.write(self.parser.data)
