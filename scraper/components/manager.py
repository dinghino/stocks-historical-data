
from scraper.settings.constants import SOURCES
from scraper.components.fetchers.base_fetcher import Fetcher
from scraper.components.parsers.base_parser import Parser

"""
Module to be used as singleton to store components coupled with a source.
"""

registered_handlers = []
available_sources = []

registered_writers = []
available_outputs = []

def register(source, fetcher_cls, parser_cls):
    if source in available_sources:
        return None

    available_sources.append(source)

    handler = Handler(source, fetcher_cls, parser_cls)
    registered_handlers.append(handler)
    return handler

def get_handlers(for_source):
    handler = next((h for h in registered_handlers if h == for_source), None)
    if not handler:
        raise Exception("Handler for '{}' were not registered. please complain.".format(for_source))
    
    return (handler.fetcher, handler.parser)

def get_sources():
    return available_sources

def reset():
    for handler in registered_handlers:
        del handler
    registered_handlers.clear()
    available_sources.clear()

class ProcessHandler:
    def __init__(self, source, fetcher_cls, parser_cls):
        if not source in SOURCES.VALID:
            raise TypeError("source should be a valid SOURCE (string)")
        if not issubclass(fetcher_cls, Fetcher):
            raise TypeError("fetcher_cls should be a subclass of Fetcher")
        if not issubclass(parser_cls, Parser):
            raise TypeError("parser_cls should be a subclass of Parser")

        # TODO: Add some way to match fetchers and parsers with the source.
        # realistically a method/property to get the source that the class is for

        self.source = source
        self.fetcher = fetcher_cls
        self.parser = parser_cls

    def __eq__(self, source_name):
        return self.source == source_name
    def __str__(self): # pragma: no cover
        return "'Handler for {}'".format(self.source)
    def __repr__(self): # pragma: no cover
        return "'<Handler for '{}' fetcher: {}, parser {} @ {}>".format(
            self.source,
            self.fetcher.__name__,
            self.parser.__name__,
            hex(id(self))
        )
    def __del__(self):
        del self.fetcher
        del self.parser
        del self

