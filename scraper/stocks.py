# from datetime import datetime as dt
import os
import datetime

from scraper.settings import Settings
from scraper.components import FinraFetcher
from scraper.components import FinraParser
from scraper.components import SingleTickerWriter, SingleFileWriter



class StockScraper:

    def __init__(self, settings, debug=False):
        
        self.settings = settings
        self._debug = debug

        self.parse_rows = self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_TICKER

    def run(self):

        self.writer = self.select_writer()(
            self.settings
        )
        self.parser = self.select_parser()(
            parse_rows=self.parse_rows
        )
        self.fetcher = self.select_fetcher()(
            settings=self.settings,
            debug=self._debug
        )

        # First row to come out is the header
        self.parser.cache_header(next(self.fetcher.run()))
        # then all the rows
        for row in self.fetcher.run():
            self.parser.parse(row, self.settings.tickers)

        self.writer.write(self.parser.data)

    def select_writer(self):
        if self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_FILE:
            return SingleFileWriter
        if self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_TICKER:
            return SingleTickerWriter
        raise Exception("There was an error setting up the file writer!")

    def select_parser(self):
        return FinraParser

    def select_fetcher(self):
        return FinraFetcher
