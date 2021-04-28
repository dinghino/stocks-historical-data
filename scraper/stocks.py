# from datetime import datetime as dt
import os
import datetime

from scraper.settings import Settings, exceptions, constants
from scraper.components import fetchers, parsers, writers, manager


class App:


    def __init__(self, settings, show_progress=True, debug=False):
        self.fetcher = None
        self.parser = None

        self.settings = settings
        self._debug = debug
        self._show_progress = show_progress
        self.parse_rows = self.settings.output_type is not constants.OUTPUT_TYPE.SINGLE_TICKER

    def run(self):

        if len(self.settings.sources) == 0:
            raise exceptions.MissingSourcesException

        self.select_writer()

        for source in self.settings.sources:

            # This raises if handlers are not registered.
            # TODO: Handle gracefully for cli feedback too
            # NOTE: For the moment handlers are registerd in scraper.__init__
            self.select_handlers(source)

            for resp in self.fetcher.run(show_progress=self._show_progress):
                self.parser.parse(resp)

            yield self.writer.write(self.parser.data, source)
            # To stay on the safe side remove everything after each source
            # has been processed
            self.clear_handlers()

    def select_writer(self):
        Writer = None
        if self.settings.output_type == constants.OUTPUT_TYPE.SINGLE_FILE:
            Writer = writers.SingleFile
        if self.settings.output_type == constants.OUTPUT_TYPE.SINGLE_TICKER:
            Writer = writers.MultiFile

        if not Writer:
            raise Exception("There was an error setting up the file writer!")
        
        self.writer = Writer(self.settings)

    def select_handlers(self, source):

        handler = manager.get_for(source)
        self.parser = handler.parser(settings=self.settings,debug=self._debug)
        self.fetcher = handler.fetcher(settings=self.settings,debug=self._debug)

    def clear_handlers(self):
        self.fetcher = None
        self.parser = None
