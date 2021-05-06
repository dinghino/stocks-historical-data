from stonks.app import App                                # noqa
from stonks.components import manager, handlers, writers  # noqa
from stonks.settings import Settings                      # noqa
from stonks.components.base_fetcher import FetcherBase    # noqa
from stonks.components.base_parser import ParserBase      # noqa
from stonks.components.base_writer import WriterBase      # noqa


def init(objects=None, modules=None, dialects=[], skip_default=False):
    """Initialize the manager with the all the available modules, adding
    the provided optional ones.
    Returns True is everything went correctly

    You can pass additional modules and ojects containing indiscrimainately
    both source handlers and writer, through the `objects` and `modules`
    arguments.

    when providing custom dialects they should be

    For modules we consider a collection of handlers (i.e. a module that
    imports more than one submodules, one for each source/writing)

    For objects we consider a single handler, so an object (or actual module!)
    containing the required classes for one source or for one output type.
    An `object` can be also an actual python module, but also a class, used
    to group stuff.

    Modules contain (and should!) objects.
    """
    done = True
    dialects = [('default', {'delimiter': '|'}), *dialects]
    done = done and manager.register_dialects_from_list(dialects)
    # register native components
    if not skip_default:
        done = done and manager.register_writers_from_module(writers)
        done = done and manager.register_handlers_from_modules(handlers)

    # ensure lists if arguments are not None
    def make_list(s):
        return None if not s else s if type(s) is list else [s]

    # process extra components provided on setup
    modules = make_list(modules)
    objects = make_list(objects)
    if modules:
        for m in modules:
            extra_m = manager.register_handlers_from_modules(m)
            extra_w = manager.register_writers_from_module(m)
            done = done and (extra_m or extra_w)
    if objects:
        for o in objects:
            extra_m = manager.register_handlers_from_obj(o)
            extra_w = manager.register_writer_from_obj(o)
            done = done and (extra_m or extra_w)

    return done
