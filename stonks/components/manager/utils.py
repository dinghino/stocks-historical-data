import inspect
from stonks.components.base_fetcher import FetcherBase
from stonks.components.base_parser import ParserBase
from stonks.components.base_writer import WriterBase


# Validation helpers
# -----------------------------------------------------------------------------
# Used internally to validate at runtime all the components and attributes
# to register components and then finding them correctly

def is_handlers_module(obj):
    return inspect.ismodule(obj) and is_handlers(obj)


def is_writers_module(obj):
    return inspect.ismodule(obj) and is_writer_object(obj)


def is_writer_object(obj):
    """ Validate an object as container for a Writer.."""
    iwo = hasattr(obj, 'output_type')
    try:
        iwo = iwo and is_writer(obj.Writer)
    except AttributeError:  # pragma: no cover
        raise TypeError(f'Missing Writer class in {obj}')
    return iwo


def is_handlers_object(obj):
    """ Validate an object as container for source handlers."""
    # NOTE: Source is required for the module to be valid. Checked explicitly
    # for separate validation of 'active' source handlers
    iho = hasattr(obj, 'source')
    try:
        iho = iho and is_parser(obj.Parser) and is_fetcher(obj.Fetcher)
    except AttributeError:
        raise TypeError(f'Missing either Fetcher or Parser class(es) in {obj}')
    return iho


def is_handlers(obj):
    """ Lazily checks if a given object can be considered a 'package' of classes
    and properties needed to register a new source.
    Object can be either a class/instance or a module."""

    is_valid = is_handlers_object(obj)
    # Validation for is_for is not required as it is an abstract static method
    # so the program would crash at launch regardless if not implemented
    is_valid = obj.Parser.is_for() == obj.source
    is_valid = obj.Fetcher.is_for() == obj.source

    if not is_valid:
        raise TypeError(
            f"Mismatched handlers in {obj.__name__} "
            "Source is {obj.source}, "
            f"Fetcher is for {obj.Fetcher.is_for()} "
            f"Parser is for {obj.Parser.is_for()}."
            )
    return is_valid


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
    return []


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
