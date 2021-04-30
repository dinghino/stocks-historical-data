from scraper.settings.constants import SOURCES, OUTPUT_TYPE
from scraper.components.fetchers.base_fetcher import Fetcher as FetcherBase
from scraper.components.parsers.base_parser import Parser as ParserBase
from scraper.components.writers.base_writer import Writer as WriterBase

"""
Module to be used as singleton to store components coupled with a source.
"""

registered_handlers = []
available_sources = []

registered_writers = []
available_outputs = []

def register_handler(source, fetcher_cls, parser_cls):
    if source in available_sources:
        return None

    available_sources.append(source)

    handler = ProcessHandler(source, fetcher_cls, parser_cls)
    registered_handlers.append(handler)
    return handler

def register_writer(output_type, writer_cls):
    if output_type in available_outputs:
        return None

    available_outputs.append(output_type)
    handler = WriterHandler(output_type, writer_cls)
    registered_writers.append(handler)
    return handler

def get_handlers(for_source=None):
    # Avoid going further since
    if not for_source in available_sources:
        raise Exception("Handler for '{}' were not registered. please complain.".format(for_source))

    handler = next((h for h in registered_handlers if h == for_source), None)
    if not handler:
        raise Exception("Handler for '{}' were not registered. please complain.".format(for_source))
    
    return (handler.fetcher, handler.parser)

def get_writer(out_type):
    if not out_type in available_outputs:
        raise Exception("Writer for '{}' were not registered. please complain.".format(out_type))
    
    handler = next((h for h in registered_writers if h == out_type), None)
    if not handler:
        raise Exception("Writer for '{}' were not registered. please complain.".format(out_type))
    
    return handler.writer

def get_sources(): # pragma: no cover
    return available_sources

def get_outputs(): # pragma: no cover
    return available_outputs

def reset():
    registered_handlers.clear()
    available_sources.clear()
    registered_writers.clear()
    available_outputs.clear()

class _HandlerBase:
    @staticmethod
    def validate_register(register, group, prefix="Handler Registrar name"):
        if not group: return True
        if register not in group:
            raise TypeError(f'{prefix} should be one of {group}')
        return True
    @staticmethod
    def validate_component_class(cls, parent_cls, cls_ref="class"):
        if not issubclass(cls, parent_cls):
            raise TypeError("fetcher_cls should be a subclass of Writer")
        return True
    @staticmethod
    def validate_component_target(target, component_cls, cls_ref="Component"):
        if not target == component_cls.is_for():
            raise TypeError(f"Provided {cls_ref} is not a match for {target}")

class WriterHandler(_HandlerBase):
    def __init__(self, type_, writer_cls):
        WriterHandler.validate_register(type_, OUTPUT_TYPE.VALID, "Output Type")
        WriterHandler.validate_component_class(writer_cls, WriterBase, "Writers")
        WriterHandler.validate_component_target(type_, writer_cls, "Writers")

        self.output_type = type_
        self.writer = writer_cls

    def __eq__(self, output_type):
        return self.output_type == output_type
    def __del__(self):
        if self.writer: del self.writer
        del self


class ProcessHandler(_HandlerBase):
    def __init__(self, source, fetcher_cls, parser_cls):
        ProcessHandler.validate_register(source, SOURCES.VALID, "Source")

        ProcessHandler.validate_component_class(fetcher_cls, FetcherBase, "Fetchers")
        ProcessHandler.validate_component_target(source, fetcher_cls, "Fetchers")

        ProcessHandler.validate_component_class(parser_cls, ParserBase, "Parsers")
        ProcessHandler.validate_component_target(source, parser_cls, "Parsers")

        # TODO: Add some way to match fetchers and parsers with the source.
        # realistically a method/property to get the source that the class is for

        self.source = source
        self.fetcher = fetcher_cls
        self.parser = parser_cls

    def __eq__(self, source_name):
        return self.source == source_name

    def __del__(self):
        if self.fetcher: del self.fetcher
        if self.parser: del self.parser
        del self

