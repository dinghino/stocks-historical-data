import inspect
from stonks.components.base_fetcher import FetcherBase
from stonks.components.base_parser import ParserBase
from stonks.components.base_writer import WriterBase


# Validation helpers
# -----------------------------------------------------------------------------
# Used internally to validate at runtime all the components and attributes
# to register components and then finding them correctly

def is_handlers_module(mod):
    return inspect.ismodule(mod) and is_handlers(mod)


def is_writers_module(mod):
    return inspect.ismodule(mod) and is_writer_object(mod)


def _hasattrs(obj, *attrs):
    for a in attrs:
        if not hasattr(obj, a):
            return False
    return True


def is_writer_object(obj):
    """ Validate an object as container for a Writer.."""
    iwo = _hasattrs(obj, 'output_type', 'Writer')
    return iwo and is_writer(obj.Writer)


def is_handlers_object(obj):
    """ Validate an object as container for source handlers."""
    # NOTE: Source is required for the module to be valid. Checked explicitly
    # for separate validation of 'active' source handlers
    iho = _hasattrs(obj, 'source', 'Parser', 'Fetcher')
    return iho and is_parser(obj.Parser) and is_fetcher(obj.Fetcher)


def is_handlers(obj):
    """ Lazily checks if a given object can be considered a 'package' of classes
    and properties needed to register a new source.
    Object can be either a class/instance or a module."""
    is_valid = False
    is_valid = is_handlers_object(obj)
    if not is_valid:    # useless to continue
        return False

    def mismatch(o):
        raise TypeError(
            f'{o.__name__} mismatch source: {obj.source} != {o.is_for()}'
        )

    parser_match = obj.Parser.is_for() == obj.source
    fetcher_match = obj.Fetcher.is_for() == obj.source
    if not parser_match or not fetcher_match:
        mismatch(obj.Fetcher)
    return is_valid and parser_match and fetcher_match


def is_parser(obj):
    """ Returns True if the provided object is a type (class) and is a subclass
    of ParserBase.
    Used to validate classes in module/objects at registration. """
    return isinstance(obj, type) and issubclass(obj, ParserBase)


def is_fetcher(obj):
    """ Returns True if the provided object is a type (class) and is a subclass
    of FetcherBase.
    Used to validate classes in module/objects at registration. """
    return isinstance(obj, type) and issubclass(obj, FetcherBase)


def is_writer(obj):
    """ Returns True if the provided object is a type (class) and is a subclass
    of WriterBase.
    Used to validate classes in module/objects at registration. """
    return isinstance(obj, type) and issubclass(obj, WriterBase)


# Registration Helpers
# -----------------------------------------------------------------------------

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
    return None


# General helpers
# -----------------------------------------------------------------------------

def get_available(container, type_):
    """
    Returns a list of all the 'target' set for all the handlers of type_.
    """
    return sorted([o['target'] for o in container if o['type'] == type_])


def validate(string, list_getter, exception):
    if string not in list_getter():
        raise exception(string, list_getter())
    return True
