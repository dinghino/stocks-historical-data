import os
import csv
from datetime import datetime

import requests
import responses

from tests.mocks.constants import (
    EXPECTED_DIR,
    SOURCES_DIR,
    TARGET_URLS,
    DATA_FILES,
    SETTINGS_PATH,
    MOCKS_PATHS,
)
from stonks import Settings
from stonks.components import manager, handlers, writers
from stonks.components import FetcherBase, ParserBase, WriterBase


class FakeFetcher(FetcherBase):
    """Simulate an actual fetcher class with required methods"""
    @staticmethod
    def is_for(): return 'test_source'

    def make_url(): pass


class FakeParser(ParserBase):
    """Simulate an actual parser class with required methods"""
    @staticmethod
    def is_for(): return 'test_source'

    def process_response_to_csv(self, response): return True

    def extract_ticker_from_row(self, row_data): return True

    def parse_row(self, row): return True


class FakeWriter(WriterBase):
    @staticmethod
    def is_for(): return 'test_output'

    def set_parse_rows(self): return True

    def write(self, header, data, source): return True


class FakeHandlerModule:
    Fetcher = FakeFetcher
    Parser = FakeParser
    source = 'test_source'
    filename_appendix = 'test_source'
    friendly_name = 'test_source'


class FakeWriterModule:
    Writer = FakeWriter
    output_type = 'test_output'
    friendly_name = 'test_output'


class WrongClass:
    pass


def get_file_path(filename, *folders):
    return os.path.join(MOCKS_PATHS, *folders, filename)


def delete_file(path):
    try:
        os.remove(path)
    except Exception:
        pass


def get_expected_start_date():
    return datetime(2021, 4, 27).date()


def get_request_urls(for_source):
    return TARGET_URLS[for_source]


def get_filenames(source, type_):
    if source not in manager.get_sources():
        raise KeyError("Invalid SOURCE for mock requested: {}".join(source))
    if type_ not in ['expected', 'source']:
        raise KeyError('Invalid TYPE for mock requested')

    # BASE = EXPECTED_DIR if type_ == 'expected' else SOURCES_DIR
    return DATA_FILES[source][type_]


def get_expected_file(filename):
    """Takes a filename and return the matching file in the EXPECTED_DIR as a
    list of lines"""
    path = os.path.join(EXPECTED_DIR, filename)
    with open(path, 'r') as file:
        # splitlines is required to get a list of lines in order to iterate
        # them in our csv.reader, similar on how the tested functions should
        # process the file
        return file.read().splitlines()


def get_expected_data_files_as_csv(source, file_idx):
    """Returns a CSV reader with the expected output for the desired source
    at the desired index on the list of available files.
    file_idx should come from the actual test function and derives from the
    response_decorator internal loop. Each url should be matched with a file"""
    file = get_expected_file(get_filenames(source, 'expected')[file_idx])
    reader = csv.reader(file)
    return reader


# responses decorator callbacks
# ----------------------------------------------------------------------------

def get_response_file(filename):
    """Takes a filename and returns the expected source file as byte-like"""
    path = os.path.join(SOURCES_DIR, filename)
    with open(path, 'rb') as file:
        return file.read()


def get_fake_response(source, index):
    file = get_response_file(get_filenames(source, "source")[index])

    def generate_response(request):  # responses actual callback function
        return (200, {}, file)
    return generate_response


# manager utilitites & decorators functions
# ----------------------------------------------------------------------------
def _manager_save_temp():
    """Closure to ensure that the previous state is kept, since this is a
    singleton. Should not matter but better safe than sorry
    """
    # Generate a new tuple to copy object and avoid references to old ones.
    temps_h = tuple(
        (o['target'], o['handler'], o['type']) for o in manager.handlers)
    temp_d = manager.get_dialects()

    def restore():
        for item in temps_h:
            manager.utils.store_handler(manager.handlers, *item)
        for name, args in temp_d:
            manager.register_dialect(name, **args)

    return restore


def clear_manager():
    manager.reset()


# =============================================================================


class decorators:
    def setup_component(component_class):
        """Setup a parser for testing using tests options for the settings."""
        def setup_component__decorator(method):
            def wrapped(self_, *args, **kwargs):
                settings = Settings(SETTINGS_PATH)
                settings.init()
                component = component_class(settings)
                return method(
                    self_, component, *args, settings=settings, **kwargs)
            return wrapped
        return setup_component__decorator

    def delete_file(*paths):
        """Utility decorator for when a test needs to write a file on disk.
        Takes an arbitrary number of FULL paths and deletes all of them before
        and after the execution of the test.
        """
        def delete_all():
            for path in paths:
                delete_file(path)

        def delete_file__decorator(method):
            def wrapped(*args, **kwargs):
                result = None
                delete_all()
                try:
                    result = method(*args, **kwargs)
                except Exception as e:
                    delete_all()
                    raise e
                delete_all()
                return result
            return wrapped
        return delete_file__decorator

    def response_decorator(source,
                           callback_generator=get_fake_response,
                           make_response=True):
        """Decorator for the tests that either perform a request or require a
        response object. Forwards to the decorated test method a fake response
        and the index of the tested url in the list of available urls."""
        def decorator(method):
            def wrapped(self_, *args, **kwargs):
                # simulate output from fetcher
                for index, url in enumerate(get_request_urls(source)):
                    responses.add_callback(
                        responses.GET,
                        url,
                        callback=callback_generator(source, index))
                    # only generate if requested (default)
                    response = None
                    if make_response:
                        response = requests.get(url, stream=True)

                    method(self_,
                           *args,
                           response=response,
                           file_num=index,
                           **kwargs)

            return wrapped
        return decorator

    def writer_data(header, data, parser_cls=handlers.finra.Parser):
        """
        Decorator to prepare data with a parser to test writer classes.
        This decorator EXPECTS to be provided with a settings object from an
        upper decorator, and it's meant to be chained BELOW setup_components
        where you setup your writer class.

        Updates settings.output_path to our tests/mocks directory
        Forwards everything it received, adding an `header` and `data`
        parameters that are meant to be used by the writer (but that can be
        obviously omitted).
        """
        def writer_data__decorator(method):
            def wrapper(*args, settings, **kwargs):
                settings.output_path = OUTPUT_DIR
                parser = parser_cls(settings)
                parser.cache_header(header)
                for row in data:
                    ticker = parser.extract_ticker_from_row(row)
                    parser.cache_data(ticker, row)
                method(*args, header=parser.header, data=parser.data, **kwargs)
            return wrapper
        return writer_data__decorator

    def register_dialect(name='default', options={'delimiter': '|'}):
        def decorator(method):
            def wrapped(*args, **kwargs):
                manager.reset()
                manager.register_dialect(name, **options)
                try:
                    method(*args, **kwargs)
                except Exception as e:
                    manager.reset()
                    raise e
                manager.reset()
            return wrapped
        return decorator

    def register_components(method):
        def wrapper(*args, **kwargs):
            manager.reset()
            manager.init(
                skip_default=True,
                objects=[handlers.finra, handlers.secftd,
                         writers.ticker_writer, writers.aggregate_writer])

            try:
                method(*args, **kwargs)
            except Exception as e:
                manager.reset()
                raise e
            manager.reset()
        return wrapper

    def manager_decorator(method):
        """decorator that saves the previous state of the manager handlers,
        execute the test and then restores it after"""
        def wrapped(*args, **kwargs):
            restore = _manager_save_temp()
            clear_manager()
            try:
                method(*args, **kwargs)
            except Exception as e:
                restore()
                raise e
            manager.reset()
        return wrapped
