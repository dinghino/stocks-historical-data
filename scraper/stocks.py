# from datetime import datetime as dt
import os
import datetime

from scraper.settings import Settings
from scraper.components import FinraFetcher, SecFtdFetcher
from scraper.components import FinraParser, SecFtdParser
from scraper.components import SingleTickerWriter, SingleFileWriter


class StockScraper:

    class MissingSourcesException(Exception):
        def __str__(self):
            return 'No Source is selected. Cannot run'

    def __init__(self, settings, debug=False):
        
        self.settings = settings
        self._debug = debug

        self.parse_rows = self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_TICKER

    def run(self):

        if len(self.settings.sources) == 0:
            raise MissingSourcesException

        self.writer = self.select_writer()(
            self.settings
        )

        for source in self.settings.sources:
            Fetcher = self.select_fetcher(source)
            Parser = self.select_parser(source)

            if not Fetcher:
                raise Exception("Cannot select Fetcher. something went wrong")
            if not Parser:
                raise Exception("Cannot select Parser. something went wrong")

            self.fetcher = Fetcher(
                settings=self.settings,
                debug=self._debug
            )
            self.parser = Parser(
                settings=self.settings,
                debug=self._debug
            )

            for response in self.fetcher.run(show_progress=True, source=source):
                self.parser.parse(response)

            self.writer.write(self.parser.data, source)

    def select_writer(self):
        if self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_FILE:
            return SingleFileWriter
        if self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_TICKER:
            return SingleTickerWriter
        raise Exception("There was an error setting up the file writer!")

    def select_parser(self, source):
        if source == Settings.SOURCES.FINRA_SHORTS:
            return FinraParser
        if source == Settings.SOURCES.SEC_FTD:
            return SecFtdParser
        return False

    def select_fetcher(self, source):
        if source == Settings.SOURCES.FINRA_SHORTS:
            return FinraFetcher
        if source == Settings.SOURCES.SEC_FTD:
            return SecFtdFetcher
        return False

