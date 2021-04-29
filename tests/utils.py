import os
import csv
from datetime import datetime

import responses, requests

from tests.mocks.constants import (
    EXPECTED_DIR,
    SOURCES_DIR,
    TARGET_URLS,
    DATA_FILES,
    SETTINGS_PATH
)
from scraper.settings.constants import SOURCES
from scraper.settings import Settings


def get_expected_start_date():
    return datetime(2021,4,27).date()

def get_request_urls(for_source):
    return TARGET_URLS[for_source]

def get_filenames(source, type_):
    if source not in SOURCES.VALID:
        raise KeyError("Invalid SOURCE for mock requested: {}".join(source))
    if type_ not in ['expected', 'source']:
        raise KeyError('Invalid TYPE for mock requested')

    BASE = EXPECTED_DIR if type_ =='expected' else SOURCES_DIR
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

# response_decorator callbacks
# ----------------------------------------------------------------------------
def get_response_file(filename):
    """Takes a filename and returns the expected source file as byte-like"""
    path = os.path.join(SOURCES_DIR, filename)
    with open(path, 'rb') as file:
        return file.read()

def get_fake_response(source, index):
    file = get_response_file(get_filenames(source, "source")[index])
    def generate_response(request): # responses actual callback function
        return (200, {}, file)
    return generate_response

def response_decorator(source, callback_generator=get_fake_response):
    """Decorator for the tests that either perform a request or require a response
    object. Forwards to the decorated test method a fake response and the index
    of the tested url in the list of available urls."""
    def decorator(func):
        def wrapped(self_, *args, **kwargs):
            # simulate output from fetcher
            for index, url in enumerate(get_request_urls(source)):
                responses.add_callback(responses.GET, url, callback=callback_generator(source, index))
                response = requests.get(url, stream=True)
                func(self_, *args, response=response, file_num=index,  **kwargs)
            return True # useless return, but for the sake of it
        return wrapped
    return decorator


def setup_parser(parser_class):
    """Setup a parser for testing using tests options for the settings."""
    def wrapper(method):
        def wrapped(self_, *args, **kwargs):
            settings = Settings(SETTINGS_PATH)
            settings.init()
            parser = parser_class(settings)
            return method(self_, *args, parser=parser, **kwargs)
        return wrapped
    return wrapper

# =============================================================================
