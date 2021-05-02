import csv
import codecs
import responses
from datetime import datetime
from stonks.constants import SOURCES
from stonks.components.handlers import finra, secftd

from tests import utils
from tests.mocks.constants import TARGET_URLS


class TestFinraFetcher:
    @utils.decorators.setup_component(finra.Fetcher)
    def test_make_url(self, fetcher, *args, **kwargs):
        # start date matches with file names
        date = utils.get_expected_start_date()
        for url in fetcher.make_url(date):
            assert url in utils.get_request_urls(SOURCES.FINRA_SHORTS)

    @utils.decorators.setup_component(finra.Fetcher)
    def test_date_range(sel_f, fetcher, *args, **kwargs):

        assert fetcher.settings.start_date == utils.get_expected_start_date()
        # Dates are the same by default on the mock options
        count = 0
        for _ in fetcher.date_range():
            count += 1
        assert count == 1

        # start is 2021,4,27
        fetcher.end_date = datetime(2021, 4, 30).date()
        count = 0
        for date in fetcher.date_range():
            count += 1
        assert count == 3

    # Base Fetcher testing functions
    @responses.activate
    @utils.decorators.setup_component(finra.Fetcher)
    @utils.decorators.response_decorator(SOURCES.FINRA_SHORTS, make_response=False) # noqa
    def test_run(self, fetcher, response, file_num, *args, **kwargs):
        # validate that the decorator is working as intended. should not
        # provide a response object, since it's the objective of the test
        assert response is None
        # validate settings
        assert fetcher.settings.start_date == utils.get_expected_start_date()

        expected_reader = utils.get_expected_data_files_as_csv(
            SOURCES.FINRA_SHORTS, file_num)

        for response in fetcher.run(show_progress=False):
            assert response is not None
            assert response.status_code == 200

            reader = csv.reader(
                codecs.iterdecode(
                    response.iter_lines(), 'utf-8', errors="replace"))
            for row in reader:
                assert row == next(expected_reader)

    @utils.decorators.setup_component(finra.Fetcher)
    def test_tickers_range(self, fetcher, *args, **kwargs):
        # NOTE: To properly test this in a loop we need something to fetch by
        # ticker. For not this is not actually available but it may be soon.
        # For coverage reason
        pass

    @utils.decorators.setup_component(finra.Fetcher)
    def test_url_validation(self, fetcher, *args, **kwargs):
        url = 'aaa'
        assert fetcher.validate_new_url('aaa') == url
        assert fetcher.validate_new_url('aaa') is None
        assert fetcher.processed == ['aaa']


class TestSecFtdFetcher:
    @utils.decorators.setup_component(secftd.Fetcher)
    def test_make_url(self, fetcher, *args, **kwargs):
        date = utils.get_expected_start_date()
        for url in fetcher.make_url(date):
            assert url in TARGET_URLS[SOURCES.SEC_FTD]
