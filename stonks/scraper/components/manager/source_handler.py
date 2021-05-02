from stonks.scraper.components.manager.handler_base import HandlerBase
from stonks.scraper.components.fetchers.base_fetcher import Fetcher
from stonks.scraper.components.parsers.base_parser import Parser
from stonks.scraper.settings.constants import SOURCES


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
