import csv
import codecs
import responses
from datetime import datetime
from stonks.components.handlers import finra

from tests import utils


class TestFinraFetcher:
    @utils.decorators.register_components
    @utils.decorators.setup_component(finra.Fetcher)
    def test_make_url(self, fetcher, *args, **kwargs):
        # start date matches with file names
        date = utils.get_expected_start_date()
        for url in fetcher.make_url(date):
            assert url in utils.get_request_urls(finra.source)

    @utils.decorators.register_components
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
    @utils.decorators.register_components
    @utils.decorators.setup_component(finra.Fetcher)
    def test_loops_generators(self, writer, *args, **kwargs):
        count = writer.get_iter_count()
        date_range = writer.get_urls_loop()
        i = sum(1 for _ in date_range())
        assert i == 1

        writer.loop_tickers_not_dates = True
        count = writer.get_iter_count()
        assert count == len(writer.settings.tickers)

        tickers_range = writer.get_urls_loop()
        assert sum(1 for _ in tickers_range()) == count

    @responses.activate
    @utils.decorators.register_components
    @utils.decorators.setup_component(finra.Fetcher)
    @utils.decorators.response_decorator(finra.source, make_response=False) # noqa
    def test_run(self, fetcher, response, file_num, *args, **kwargs):
        # validate that the decorator is working as intended. should not
        # provide a response object, since it's the objective of the test
        assert response is None
        # validate settings
        assert fetcher.settings.start_date == utils.get_expected_start_date()

        expected_reader = utils.get_expected_data_files_as_csv(
            finra.source, file_num)

        for result in fetcher.run(show_progress=False):
            assert result.response is not None
            assert result.response.status_code == 200

        for result in fetcher.run(show_progress=True):
            assert result.response is not None
            assert result.response.status_code == 200

            reader = csv.reader(
                codecs.iterdecode(
                    result.response.iter_lines(), 'utf-8', errors="replace"))

            for row in reader:
                assert row == next(expected_reader)

    @utils.decorators.register_components
    @utils.decorators.setup_component(finra.Fetcher)
    def test_tickers_range(self, fetcher, *args, **kwargs):
        # NOTE: To properly test this in a loop we need something to fetch by
        # ticker. For not this is not actually available but it may be soon.
        # For coverage reason
        pass

    @utils.decorators.register_components
    @utils.decorators.setup_component(finra.Fetcher)
    def test_url_validation(self, fetcher, *args, **kwargs):
        url = 'aaa'
        assert fetcher.validate_new_url(url) == url
        assert fetcher.validate_new_url(url) is None
        assert fetcher.processed == [url]
