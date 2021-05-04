import csv
import inspect

from stonks.components.manager.handler_base import HandlerBase # noqa
from stonks.components.manager.source_handler import SourceHandler
from stonks.components.manager.writer_handler import WriterHandler
from stonks.components.manager import utils
from stonks import exceptions

"""
Module to be used as singleton to store components coupled with a source.
"""

__H_T_SOURCE = 'source_handler'
__H_T_WRITER = 'writer_handler'

# {'type': '__H_T_XXXX', 'target': 'source/out_type', 'handler': HandlerClass}
handlers = []

# {name: {arg dict}}
csv_dialects = []


# Registration methods - from modules and object
# -----------------------------------------------------------------------------
# Primary and preffered way of registering components for the application


def register_writers_from_module(module):
    """ Utility function to automate loading writers from an import.
        Automatically detect all WriterBase subclasses present in the module
        and registers them with the manager. """
    for _, obj in inspect.getmembers(module, utils.is_writers_module):
        register_writer_from_obj(obj)
    return True


def register_handlers_from_modules(module):
    """  Utility function to automate loading Parsers and Fetcher from the whole
        'handlers' module. Use this method if you want to import as
        `from stonks.components import handlers`
        and register all the available modules.
    """
    for _, obj in inspect.getmembers(module, utils.is_handlers_module):
        register_handlers_from_obj(obj)
    return True


def register_handlers_from_obj(obj):
    """ Utility function to automate loading Parsers and Fetcher from a single
        'handler' module. Meant to be used when importing as
        `from stonks.components.handlers import <name>`
        But can also be used on any object that contains a `Parser` and
        `Fetcher`property containing the right subclasses objects
        (not instances!) like
        ```
        class A:
            Parser = <ParserBase_Subclass>
            Fetcher = <FetcherBase_Subclass>
            ...
        ```
    """
    if not utils.is_handlers(obj):
        return None
    if obj.source in get_sources():  # pragma: no cover # noqa
        return None

    handler = SourceHandler.get_from_object(obj)
    utils.store_handler(handlers, obj.source, handler, __H_T_SOURCE)
    return True


def register_writer_from_obj(obj):
    if not utils.is_writer_object(obj):
        return None
    if obj.output_type in get_outputs():  # pragma: no cover
        return None

    handler = WriterHandler.get_from_object(obj)
    utils.store_handler(handlers, obj.output_type, handler, __H_T_WRITER)
    return True


def register_dialects_from_list(dialects):
    """Takes an iterable of list/tuple [(name, {**arguments})] to register."""
    for name, kwargs in dialects:
        register_dialect(name, **kwargs)
    return True


def register_dialect(name, **kwargs):
    """ Store a new csv dialect to be later processed. Avoid duplicates. """
    if name in get_dialects_list():
        raise ValueError(f'Dialect {name} already registered.')

    csv_dialects.append({'name': name, 'args': kwargs})
    csv.register_dialect(name, **kwargs)
    return True


# Registration methods - raw registration
# -----------------------------------------------------------------------------
# Internal method that actually perform the registration

def register_handler(
        source, fetcher_cls, parser_cls,
        appendix, description="", friendly=""):

    if source in get_sources():
        return None

    handler = SourceHandler(
        source=source,
        fetcher_cls=fetcher_cls,
        parser_cls=parser_cls,
        filename_appendix=appendix,
        friendly=friendly,
        description=description
    )
    utils.store_handler(handlers, source, handler, __H_T_SOURCE)
    return handler


def register_writer(output_type, writer_cls, description="", friendly=""):

    if output_type in get_outputs():  # pragma: no cover
        return None

    handler = WriterHandler(
        type_=output_type,
        writer_cls=writer_cls,
        description=description,
        friendly=friendly
        )
    utils.store_handler(handlers, output_type, handler, __H_T_WRITER)

    return handler


# Validation methods
# -----------------------------------------------------------------------------
# Validation functions. Used to check if components are registered for a given
# request

def validate_source(source):
    return utils.validate(
        source, get_sources, exceptions.SourceException)


def validate_output(output_type):
    return utils.validate(
        output_type, get_outputs, exceptions.OutputTypeException)


def validate_dialect(dialect):
    return utils.validate(
            dialect, get_dialects_list, exceptions.DialectException)


# Availability getters
# -----------------------------------------------------------------------------


def get_dialects():
    """ Return a tuple of (name, args) for all registered dialects. """
    return tuple(tuple(item.values()) for item in csv_dialects)


def get_dialects_list():
    """ Return a tuple with all the available dialect names registered. """
    registered = tuple(i['name'] for i in csv_dialects)
    # remove duplicated, since the ones we register through the manager
    # could (should) be set in csv module too
    unique = set([*registered, *csv.list_dialects()])
    return tuple(unique)

# Component getters
# -----------------------------------------------------------------------------


def get_handlers(for_source):
    handler = utils.get_handler(handlers, __H_T_SOURCE, for_source)

    if not handler:
        raise Exception(
            "Handlers for '{}' were not registered."
            " please complain.".format(for_source))

    return (handler.fetcher, handler.parser)


def get_writer(out_type):

    handler = utils.get_handler(handlers, __H_T_WRITER, out_type)
    if not handler:
        raise Exception(
            "Writer for '{}' were not registered."
            " please complain.".format(out_type))

    return handler.writer


def get_sources():  # pragma: no cover
    return utils.get_available(handlers, __H_T_SOURCE)
    # return available_sources


def get_outputs():  # pragma: no cover
    return utils.get_available(handlers, __H_T_WRITER)
    # return available_outputs


def get_all_handlers():
    """ Returns a list with all the registered source handler objects. """
    return [o['handler'] for o in handlers if o['type'] == __H_T_SOURCE]


def get_all_writers():
    """ Returns a list with all the registered writers handler objects. """
    return [o['handler'] for o in handlers if o['type'] == __H_T_WRITER]


def get_filename_source_appendix(source):
    handler = utils.get_handler(handlers, __H_T_SOURCE, source)
    return handler.filename_appendix if handler else ""


def reset():
    handlers.clear()
    for name in (i['name'] for i in csv_dialects):
        csv.unregister_dialect(name)
    csv_dialects.clear()
