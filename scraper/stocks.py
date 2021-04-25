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

        self.writer = self._WriterClass(self.settings)
        self.parser = FinraParser(strip_ticker=self._strip_ticker_when_parsing)

        self.fetcher = Fetcher(
            parser=self.parser,
            settings=self.settings,
            debug=self._debug
        )

        self.fetcher.run()
        self.writer.write(self.parser.data)
