import inspect
from stonks import manager


def register_writers_from_module(module):
    for name, cls in inspect.getmembers(module, inspect.isclass):
        try:
            manager.register_writer(cls.is_for(), cls)
        except Exception as e:
            print(f"Error while registering '{name} as WRITER in cli/cli.py")
            raise e


def register_handlers_from_module(module):
    for name, mod in inspect.getmembers(module, inspect.ismodule):
        try:
            source = mod.Parser.is_for()
            manager.register_handler(source, mod.Fetcher, mod.Parser)
        except Exception as e:
            print(f"Error while registering '{name} HANDLERS in cli/cli.py")
            raise e


def register_dialects_from_dict(dialects):
    for name, props in dialects:
        manager.register_dialect(name, **props)


def setup(handlers_module, writers_module, dialects_dict={}):
    register_handlers_from_module(handlers_module)
    register_writers_from_module(writers_module)
    register_dialects_from_dict(dialects_dict)
