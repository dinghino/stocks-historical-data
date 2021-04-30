from scraper.components.manager.handler_base import HandlerBase # noqa
from scraper.components.manager.source_handler import SourceHandler
from scraper.components.manager.writer_handler import WriterHandler


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

    handler = SourceHandler(source, fetcher_cls, parser_cls)
    registered_handlers.append(handler)
    return handler


def register_writer(output_type, writer_cls):
    if output_type in available_outputs:  # pragma: no cover
        return None

    available_outputs.append(output_type)
    handler = WriterHandler(output_type, writer_cls)
    registered_writers.append(handler)
    return handler


def get_handlers(for_source=None):
    # Avoid going further since
    if for_source not in available_sources:
        raise Exception(
            "Handler for '{}' were not registered."
            " please complain.".format(for_source))

    handler = next((h for h in registered_handlers if h == for_source), None)
    if not handler:  # pragma: no cover
        raise Exception(
            "Handler for '{}' were not registered."
            " please complain.".format(for_source))

    return (handler.fetcher, handler.parser)


def get_writer(out_type):
    if out_type not in available_outputs:
        raise Exception(
            "Writer for '{}' were not registered."
            " please complain.".format(out_type))

    handler = next((h for h in registered_writers if h == out_type), None)
    if not handler:  # pragma: no cover
        raise Exception(
            "Writer for '{}' were not registered."
            " please complain.".format(out_type))

    return handler.writer


def get_sources():  # pragma: no cover
    return available_sources


def get_outputs():  # pragma: no cover
    return available_outputs


def reset():
    registered_handlers.clear()
    available_sources.clear()
    registered_writers.clear()
    available_outputs.clear()
