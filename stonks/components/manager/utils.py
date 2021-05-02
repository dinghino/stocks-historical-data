import inspect
from stonks.components import WriterBase, ParserBase, FetcherBase


def is_handlers_package(obj):
    return inspect.ismodule(obj) and is_handler(obj)


def is_handler(obj):
    try:
        if is_parser(obj.Parser) and is_fetcher(obj.Fetcher):
            if obj.Parser.is_for() == obj.Fetcher.is_for():
                return True
    except Exception:  # pragma: no cover
        pass

    raise TypeError(f"Mismatched handlers in {obj.__name__} ({obj})")


def is_parser(obj):
    return isinstance(obj, type) and issubclass(obj, ParserBase)


def is_fetcher(obj):
    return isinstance(obj, type) and issubclass(obj, FetcherBase)


def is_writer(obj):
    return isinstance(obj, type) and issubclass(obj, WriterBase)


def store_handler(container, target, handler, type_):
    container.append(
        {"type": type_, "target": target, "handler": handler}
    )


def get_handler(container, type_, target):
    def match(item):
        return item['type'] == type_ and item['target'] == target

    found = [obj['handler'] for obj in container if match(obj)]
    if found:  # fails if empty list
        return found[0]
    return []


def get_available(container, type_):
    """
    Returns a list of all the 'target' set for all the handlers of type_.
    """
    return [o['target'] for o in container if o['type'] == type_]
