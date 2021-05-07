# from tests.utils import FakeFetcher as Fetcher   # noqa
# from tests.utils import FakeParser as Parser     # noqa
from stonks.components import FetcherBase, ParserBase


class Fetcher(FetcherBase):
    """Simulate an actual fetcher class with required methods"""
    @staticmethod
    def is_for(): return 'test_source'

    def make_url(): pass


class Parser(ParserBase):
    """Simulate an actual parser class with required methods"""
    @staticmethod
    def is_for(): return 'test_source'

    def process_response_to_csv(self, response): return True

    def extract_ticker_from_row(self, row_data): return True

    def parse_row(self, row): return True


source = Parser.is_for()
filename_appendix = Parser.is_for()
