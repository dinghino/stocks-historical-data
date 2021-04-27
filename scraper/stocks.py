# from datetime import datetime as dt
import os
import datetime

from scraper.settings import Settings
from scraper.components import fetchers
from scraper.components import parsers
from scraper.components import writers


class StockScraper:

    class MissingSourcesException(Exception):
        def __str__(self):
            return 'No Source is selected. Cannot run'

    def __init__(self, settings, show_progress=True, debug=False):
        
        self.settings = settings
        self._debug = debug
        self._show_progress = show_progress
        self.parse_rows = self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_TICKER

    def run(self):

        if len(self.settings.sources) == 0:
            raise StockScraper.MissingSourcesException

        self.select_writer()

        for source in self.settings.sources:
            
            self.select_fetcher(source)
            self.select_parser(source)

            responses = self.fetcher.run(show_progress=self._show_progress)
            for resp in responses:
                self.parser.parse(resp)

            yield self.writer.write(self.parser.data, source)

    def select_writer(self):
        Cls = None
        if self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_FILE:
            Cls = writers.SingleFile
        if self.settings.output_type == Settings.OUTPUT_TYPE.SINGLE_TICKER:
            Cls = writers.MultiFile

        if not Cls:
            raise Exception("There was an error setting up the file writer!")
        
        self.writer = Cls(self.settings)

    def select_parser(self, source):
        Cls = None
        if source == Settings.SOURCES.FINRA_SHORTS:
            Cls = parsers.Finra
        elif source == Settings.SOURCES.SEC_FTD:
            Cls = parsers.SecFtd

        if not Cls:
            raise Exception("There was an error setting up the Parser class!")
        self.parser = Cls(settings=self.settings,debug=self._debug)
        return True

    def select_fetcher(self, source):
        Cls = None
        if source == Settings.SOURCES.FINRA_SHORTS:
            Cls = fetchers.Finra
        elif source == Settings.SOURCES.SEC_FTD:
            Cls = fetchers.SecFtd
        
        if Cls is None:
            raise Exception("There was an error setting up the Fetcher class!")
        
        self.fetcher = Cls(settings=self.settings,debug=self._debug)
        return True
