import pytest
import responses
from tests import utils
from stonks.constants import SOURCES
from stonks.components import finra

HEADER_SOURCE = [
    "Date",
    "Symbol",
    "ShortVolume",
    "ShortExemptVolume",
    "TotalVolume",
    "Market"]
HEADER_MULTI = [
    "Date",
    "Symbol",
    "ShortVolume",
    "ShortExemptVolume",
    "TotalVolume",
    "Market"]
HEADER_SINGLE = [
    "Date",
    "ShortVolume",
    "ShortExemptVolume",
    "TotalVolume"]
ROW_SOURCE = ["20210427", "AA", "992738", "619", "2029539", "B,Q,N"]
ROW_MULTI = ["2021-04-27", "AA", "992738", "619", "2029539", "B,Q,N"]
ROW_SINGLE = ["2021-04-27", "992738", "619", "2029539"]


class TestFinraParser:
    @responses.activate
    @utils.decorators.setup_component(finra.Parser)
    @utils.decorators.response_decorator(SOURCES.FINRA_SHORTS)
    def test_process_to_csv(self, parser, response, file_num, *args, **kwargs):
        expected_rows = utils.get_expected_data_files_as_csv(
            SOURCES.FINRA_SHORTS, file_num)
        parsed_rows = parser.process_response_to_csv(response)

        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            expected_row = next(expected_rows)
            assert parsed_row == expected_row

    @utils.decorators.setup_component(finra.Parser)
    def test_extract_ticker_from_row(self, parser, *args, **kwargs):
        row_data = ROW_SOURCE
        assert parser.extract_ticker_from_row(row_data) == "AA"

    @utils.decorators.setup_component(finra.Parser)
    def test_parse_row(self, parser, *args, **kwargs):
        # parser._parse_rows is set to True by the mock Settings options
        assert parser._parse_rows is True
        # Parse everything and remove the symbol.
        # used to write one symbol per file
        assert parser.parse_row(ROW_SOURCE) == ROW_SINGLE

        # Parse the date but keep the symbol.
        # used to write more symbols on single file
        parser._parse_rows = False
        assert parser.parse_row(ROW_SOURCE) == ROW_MULTI

    @utils.decorators.setup_component(finra.Parser)
    def test_parse_headers(self, parser, *args, **kwargs):

        assert parser._parse_rows is True
        assert (
            parser.parse_headers(HEADER_SOURCE) == HEADER_SINGLE)
        parser._parse_rows = False
        assert (
            parser.parse_headers(HEADER_SOURCE) == HEADER_MULTI)

    @utils.decorators.setup_component(finra.Parser)
    def test_get_row_date(self, parser, *args, **kwargs):
        # custom row, simulate already parsed row
        row = ["2021-04-27", "AA", "992738", "619", "2029539", "B,Q,N"]
        expected = '2021-04-27'
        parser.cache_header(HEADER_SOURCE)
        date = parser.get_row_date(row)
        assert date == expected

        # Test with different positions
        parser._header = []
        header = ["DERP"] + HEADER_SOURCE
        row = ["dork", "2021-04-27"] + ROW_SOURCE[1:]
        parser.cache_header(header)
        date = parser.get_row_date(row)
        assert date == expected

        with pytest.raises(ValueError):
            parser._header = []
            parser.get_row_date(row)
        with pytest.raises(ValueError):
            parser._header = ["Not", "valid"]
            parser.get_row_date(row)

    @utils.decorators.setup_component(finra.Parser)
    def test_data_caching(self, parser, *args, **kwargs):
        assert parser._parse_rows is True
        parser.cache_header(HEADER_SOURCE)
        assert parser.header == HEADER_SINGLE

        parser.cache_data("AA", ROW_SOURCE)
        assert "AA" in parser.data
        assert parser.data["AA"] == [ROW_SINGLE]
        # Attempt duplicating the row. should fail, based on input date
        parser.cache_data("AA", ROW_SOURCE)
        assert len(parser.data.keys()) == 1
        # Duplicated row should not be included. matching is done with date
        assert parser.data["AA"] == [ROW_SINGLE]

    @responses.activate
    @utils.decorators.setup_component(finra.Parser)
    @utils.decorators.response_decorator(SOURCES.FINRA_SHORTS)
    def test_parse(self, parser, response, file_num, *args, **kwargs):
        parser.settings.clear_tickers()
        for ticker in ["AMC", "GME"]:
            parser.settings.add_ticker(ticker)

        parser.parse(response)
        assert parser._parse_rows is True
        assert "GME" in parser.data.keys()
        assert "AMC" in parser.data.keys()
        assert "AA" not in parser.data.keys()

        assert parser.header == HEADER_SINGLE
        assert parser.data["GME"] == [['2021-04-27', '2291953', '44637', '3972777']]  # noqa
