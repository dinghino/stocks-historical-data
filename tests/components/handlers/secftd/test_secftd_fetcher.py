from stonks.components.handlers import secftd

from tests import utils

# NOTE: The majority of the tests for the base fetcher is being run with
# the tests for FinraFetcher and not duplicated for obvious reasons.


class TestSecFtdFetcher:
    @utils.decorators.register_components
    @utils.decorators.setup_component(secftd.Fetcher)
    def test_make_url(self, fetcher, *args, **kwargs):
        date = utils.get_expected_start_date()
        for url in fetcher.make_url(date):
            assert url in utils.get_request_urls(secftd.source)
