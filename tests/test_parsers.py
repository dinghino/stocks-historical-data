import pytest
import responses
from functools import wraps
from tests import mocks, utils
from scraper.settings.constants import SOURCES

from scraper.settings import Settings
from scraper.components import parsers

def fail():
    assert True == False

class TestFinraParser:

    @responses.activate
    @utils.response_decorator(SOURCES.FINRA_SHORTS)
    def test_process_to_csv(self, response, iteration):
        settings = Settings(mocks.constants.SETTINGS_PATH)
        settings.init()


        parser = parsers.Finra(settings)

        expected_rows = utils.get_expected_data_files_as_csv(SOURCES.FINRA_SHORTS, iteration)
        parsed_rows = parser.process_response_to_csv(response)
        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            expected_row = next(expected_rows)
            assert parsed_row == expected_row


class TestSecFtdParser:

    @responses.activate
    @utils.response_decorator(SOURCES.SEC_FTD)
    def test_process_to_csv(self, response, iteration):
        settings = Settings(mocks.constants.SETTINGS_PATH)
        settings.init()

        parser = parsers.SecFtd(settings)
        expected_rows = utils.get_expected_data_files_as_csv(SOURCES.SEC_FTD, iteration)
        parsed_rows = parser.process_response_to_csv(response)
        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            assert parsed_row == next(expected_rows)
