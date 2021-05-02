from stonks.components.manager.handler_base import HandlerBase
from stonks.components.base_fetcher import FetcherBase
from stonks.components.base_parser import ParserBase
from stonks.constants import SOURCES


class SourceHandler(HandlerBase):

    def __init__(self, source, fetcher_cls, parser_cls):
        SourceHandler.validate_register(source, SOURCES.VALID, "Source")

        SourceHandler.validate_component_class(
            fetcher_cls, FetcherBase, "Fetchers")
        SourceHandler.validate_component_target(
            source, fetcher_cls, "Fetchers")

        SourceHandler.validate_component_class(
            parser_cls, ParserBase, "Parsers")
        SourceHandler.validate_component_target(
            source, parser_cls, "Parsers")

        self.source = source
        self.fetcher = fetcher_cls
        self.parser = parser_cls

    def __repr__(self):
        parser = self.parser.__name__
        fetcher = self.fetcher.__name__
        source = self.source

        return f'<SourceHandler | {source} - {fetcher}, {parser}>'
