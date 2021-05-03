from stonks import exceptions
from stonks.components import manager


class App:
    def __init__(self, settings, show_progress=False, debug=False):
        self.fetcher = None
        self.parser = None

        self.settings = settings
        self._debug = debug
        self._show_progress = show_progress

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

            yield self.writer.write(
                self.parser.header, self.parser.data, source)
            # To stay on the safe side remove everything after each source
            # has been processed
            self.clear_handlers()

    def select_writer(self):
        # TODO: Add exception handling for when we'll have more writer options
        self.writer = manager.get_writer(
            self.settings.output_type)(self.settings)

    def select_handlers(self, source):
        # TODO: Add exception handling for when we'll have more dynamic
        # handlers
        fetcher_cls, parser_cls = manager.get_handlers(source)
        self.fetcher = fetcher_cls(
            settings=self.settings, debug=self._debug)
        self.parser = parser_cls(
            settings=self.settings, debug=self._debug)

    def clear_handlers(self):
        self.fetcher = None
        self.parser = None
