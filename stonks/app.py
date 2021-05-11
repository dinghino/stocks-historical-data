from stonks import exceptions
from stonks.components import manager


class App:
    PROCESSING = "APP__PROCESSING"
    DONE = "APP__DONE"
    ERROR = "APP__ERROR"

    STATES = [PROCESSING, DONE, ERROR]

    class Result:
        def __init__(self, state, source, done):
            self.state = state
            self.source = source
            self.done = done

    def __init__(self, settings, show_progress=False, debug=False):
        self.fetcher = None
        self.parser = None

        self.settings = settings
        self._debug = debug
        self._show_progress = show_progress

    def run(self):
        if len(self.settings.sources) == 0:
            raise exceptions.MissingSourcesException

        if not self.settings.validate():  # pragma: no cover
            yield App.Result(App.ERROR, None, False)

        self.select_writer()

        for source in self.settings.sources:
            yield App.Result(App.PROCESSING, source, False)
            self.select_handlers(source)

            for resp in self.fetcher.run(show_progress=self._show_progress):
                self.parser.parse(resp)

            write_ops = self.writer.write(
                self.parser.header,
                self.parser.data,
                source)

            for write_result in write_ops:
                yield App.Result(App.DONE, source, write_result)
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
