from stonks import exceptions
from stonks.components import manager


class App:
    PROCESSING = "APP__PROCESSING"
    DONE = "APP__DONE"
    ERROR = "APP__ERROR"

    STATES = [PROCESSING, DONE, ERROR]

    class Result:
        def __init__(
              self, state, source=None, done=False, message="", tickers=[]):

            self.state = state
            self.source = source
            self.done = done
            self.tickers = tickers
            self.message = message

    def __init__(self, settings, show_progress=False, debug=False):
        self.fetcher = None
        self.parser = None

        self.settings = settings
        self._debug = debug
        self._show_progress = show_progress

    def run(self):
        if len(self.settings.sources) == 0:
            yield App.Result(App.ERROR, message='No sources available')
            raise exceptions.MissingSourcesException

        if not self.settings.validate():  # pragma: no cover
            yield App.Result(App.ERROR, message='Settings are not valid.')
            return

        self.select_writer()

        for source in self.settings.sources:
            yield App.Result(App.PROCESSING, source, False)
            self.select_handlers(source)

            for result in self.fetcher.run(show_progress=self._show_progress):
                if result.done:
                    self.parser.parse(result.response)

            header, data = self.parser.header, self.parser.data
            for result in self.writer.write(header, data, source):
                if result.success:
                    yield App.Result(
                        App.DONE, source, result.success, result.message,
                        (result.tickers or self.settings.tickers))
                    continue
                # else:
                yield App.Result(
                    App.ERROR, source, result.success, result.message,
                    (result.tickers or self.settings.tickers))

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
