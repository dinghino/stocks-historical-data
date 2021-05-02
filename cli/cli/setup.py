from stonks.components import manager, writers, handlers


def setup(handlers_module=None, writers_module=None, dialects=[]):
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
