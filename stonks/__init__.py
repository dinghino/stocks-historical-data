from stonks.app import App                                # noqa
from stonks.components import manager, handlers, writers  # noqa
from stonks.settings import Settings                      # noqa
from stonks.components.base_fetcher import FetcherBase    # noqa
from stonks.components.base_parser import ParserBase      # noqa
from stonks.components.base_writer import WriterBase      # noqa


def init(handlers_module=None, writers_module=None, dialects=[]):
    """Initialize the manager with the all the available modules, adding
    the provided optional ones.
    Returns True is everything went corretly
    """
    done = True
    dialects = [('default', {'delimiter': '|'}), *dialects]
    # register native components
    done = done and manager.register_dialects_from_list(dialects)
    done = done and manager.register_writers_from_module(writers)
    done = done and manager.register_handlers_from_modules(handlers)

    # process extra components provided on setup
    if handlers_module:
        done = done and manager.register_handlers_from_modules(handlers_module)
    if writers_module:
        done = done and manager.register_writers_from_module(writers_module)

    return done
