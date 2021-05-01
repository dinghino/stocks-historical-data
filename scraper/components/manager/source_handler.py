from scraper.components.manager.handler_base import HandlerBase
from scraper.components.fetchers.base_fetcher import Fetcher
from scraper.components.parsers.base_parser import Parser
from scraper.settings.constants import SOURCES


class SourceHandler(HandlerBase):

    def __init__(self, source, fetcher_cls, parser_cls):
        SourceHandler.validate_register(source, SOURCES.VALID, "Source")

        SourceHandler.validate_component_class(
            fetcher_cls, Fetcher, "Fetchers")
        SourceHandler.validate_component_target(
            source, fetcher_cls, "Fetchers")

        SourceHandler.validate_component_class(
            parser_cls, Parser, "Parsers")
        SourceHandler.validate_component_target(
            source, parser_cls, "Parsers")

        self.source = source
        self.fetcher = fetcher_cls
        self.parser = parser_cls

    def __eq__(self, source_name):
        return self.source == source_name

    def __del__(self):
        self.fetcher and self.fetcher
        self.parser and self.parser
        del self
