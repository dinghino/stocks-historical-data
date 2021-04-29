import csv
import codecs
import pytest
import responses
from datetime import datetime
from scraper.settings.constants import SOURCES
from scraper.settings import Settings
from scraper.components import fetchers

from tests import mocks, utils
from tests.mocks.constants import TARGET_URLS


class TestFinraFetcher:
    @utils.setup_component(fetchers.Finra)
    def test_make_url(self, fetcher):
        # start date matches with file names
        date = utils.get_expected_start_date()
        for url in fetcher.make_url(date):
            assert url in utils.get_request_urls(SOURCES.FINRA_SHORTS)

    @utils.setup_component(fetchers.Finra)
    def test_date_range(sel_f, fetcher):

        assert fetcher.settings.start_date == utils.get_expected_start_date()
        # Dates are the same by default on the mock options
        count = 0
        for _ in fetcher.date_range(): count +=1
        assert count == 1

        # start is 2021,4,27
        fetcher.end_date = datetime(2021,4,30).date()
        count = 0
        for date in fetcher.date_range(): count +=1
        assert count == 3


    # Base Fetcher testing functions
    @responses.activate
    @utils.setup_component(fetchers.Finra)
    @utils.response_decorator(SOURCES.FINRA_SHORTS, make_response=False)
    def test_run(self, fetcher, response, file_num):
        # validate that the decorator is working as intended. should not provide
        # a response object, since it's the objective of the test
        assert response is None
        # validate settings
        assert fetcher.settings.start_date == utils.get_expected_start_date()

        expected_reader = utils.get_expected_data_files_as_csv(SOURCES.FINRA_SHORTS, file_num)

        for response in fetcher.run(show_progress=False):
            assert response is not None
            assert response.status_code == 200

            reader = csv.reader(codecs.iterdecode(response.iter_lines(), 'utf-8', errors="replace"))
            for row in reader:
                assert row == next(expected_reader)

    @utils.setup_component(fetchers.Finra)
    def test_tickers_range(self, fetcher):
        # NOTE: To properly test this in a loop we need something to fetch by ticker.
        # For not this is not actually available but it may be soon. For coverage reason
        pass


    @utils.setup_component(fetchers.Finra)
    def test_url_validation(self, fetcher):
        url = 'aaa'
        assert fetcher.validate_new_url('aaa') == url
        assert fetcher.validate_new_url('aaa') == None
        assert fetcher.processed == ['aaa']



class TestSecFtdFetcher:
    @utils.setup_component(fetchers.SecFtd)
    def test_make_url(self, fetcher):
        date = utils.get_expected_start_date()
        for url in fetcher.make_url(date):
            assert url in TARGET_URLS[SOURCES.SEC_FTD]
