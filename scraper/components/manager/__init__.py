from scraper.components.manager.handler_base import HandlerBase # noqa
from scraper.components.manager.source_handler import SourceHandler
from scraper.components.manager.writer_handler import WriterHandler


"""
Module to be used as singleton to store components coupled with a source.
"""
__H_T_SOURCE = 'source_handler'
__H_T_WRITER = 'writer_handler'

# {'type': '__H_T_XXXX', 'target': 'source/out_type', 'handler': HandlerClass}
handlers = []

# {name: {arg dict}}
csv_dialects = []


def register_dialect(name, **kwargs):
    """ Store a new csv dialect to be later processed. Avoid duplicates. """
    if name in get_dialects_list():
        raise ValueError(f'Dialect {name} already registered.')

    csv_dialects.append({'name': name, 'args': kwargs})
    return True


def get_dialects():
    """ Return a tuple of (name, args) for all registered dialects. """
    return tuple(tuple(item.values()) for item in csv_dialects)


def get_dialects_list():
    """ Return a tuple with all the available dialect names registered. """
    return tuple(i['name'] for i in csv_dialects)


def _store_handler(target, handler, type_):
    print(f"Adding {type_} for {target}")
    handlers.append(
        {"type": type_, "target": target, "handler": handler}
    )


def _get_handler(type_, target):
    def match(item):
        return item['type'] == type_ and item['target'] == target

    found = [obj['handler'] for obj in handlers if match(obj)]
    if found:  # fails if empty list
        return found[0]
    return []


def _get_available(type_):
    """
    Returns a list of all the 'target' set for all the handlers of type_.
    """
    return [o['target'] for o in handlers if o['type'] == type_]


def register_handler(source, fetcher_cls, parser_cls):

    if source in get_sources():
        return None

    handler = SourceHandler(source, fetcher_cls, parser_cls)
    _store_handler(source, handler, __H_T_SOURCE)
    return handler


def register_writer(output_type, writer_cls):

    if output_type in get_outputs():  # pragma: no cover
        return None

    handler = WriterHandler(output_type, writer_cls)
    _store_handler(output_type, handler, __H_T_WRITER)

    return handler


def get_handlers(for_source):
    handler = _get_handler(__H_T_SOURCE, for_source)

    if not handler:
        raise Exception(
            "Handlers for '{}' were not registered."
            " please complain.".format(for_source))

    return (handler.fetcher, handler.parser)


def get_writer(out_type):

    handler = _get_handler(__H_T_WRITER, out_type)
    if not handler:
        raise Exception(
            "Writer for '{}' were not registered."
            " please complain.".format(out_type))

    return handler.writer


def get_sources():  # pragma: no cover
    return _get_available(__H_T_SOURCE)
    # return available_sources


def get_outputs():  # pragma: no cover
    return _get_available(__H_T_WRITER)
    # return available_outputs


def get_all_handlers():
    """ Returns a list with all the registered source handler objects. """
    return [o['handler'] for o in handlers if o['type'] == __H_T_SOURCE]


def get_all_writers():
    """ Returns a list with all the registered writers handler objects. """
    return [o['handler'] for o in handlers if o['type'] == __H_T_WRITER]


def reset():
    handlers.clear()
    csv_dialects.clear()
