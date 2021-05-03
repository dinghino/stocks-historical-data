from stonks.components.manager.handler_base import HandlerBase
from stonks.components.base_fetcher import FetcherBase
from stonks.components.base_parser import ParserBase


class SourceHandler(HandlerBase):

    def __init__(
            self, source, fetcher_cls, parser_cls, fn_apx, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.filename_appendix = fn_apx
        # TODO: Validate uniqueness for friendly_name [and appendix]

        SourceHandler.validate_component_class(
            source, fetcher_cls, FetcherBase, "Fetcher")

        SourceHandler.validate_component_class(
            source, parser_cls, ParserBase, "Parser")

        self.source = source
        self.fetcher = fetcher_cls
        self.parser = parser_cls

    def __repr__(self):
        parser = self.parser.__name__
        fetcher = self.fetcher.__name__
        source = self.source

        return f'<SourceHandler | {source} - {fetcher}, {parser}>'
