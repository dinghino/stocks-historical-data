import pytest
import responses
from tests import utils
from scraper.settings.constants import SOURCES

from scraper.components import parsers
HEADER_FINRA__SOURCE = [
    "Date",
    "Symbol",
    "ShortVolume",
    "ShortExemptVolume",
    "TotalVolume",
    "Market"]
HEADER_FINRA__MULTI = [
    "Date",
    "Symbol",
    "ShortVolume",
    "ShortExemptVolume",
    "TotalVolume",
    "Market"]
HEADER_FINRA__SINGLE = [
    "Date",
    "ShortVolume",
    "ShortExemptVolume",
    "TotalVolume"]
ROW_FINRA__SOURCE = ["20210427", "AA", "992738", "619", "2029539", "B,Q,N"]
ROW_FINRA__MULTI = ["2021-04-27", "AA", "992738", "619", "2029539", "B,Q,N"]
ROW_FINRA__SINGLE = ["2021-04-27", "992738", "619", "2029539"]

HEADER_SEC__SOURCE = [
    "SETTLEMENT DATE",
    "CUSIP",
    "SYMBOL",
    "QUANTITY (FAILS)",
    "DESCRIPTION",
    "PRICE"]
HEADER_SEC__MULTI = [
    "SETTLEMENT DATE",
    "CUSIP",
    "SYMBOL",
    "QUANTITY (FAILS)",
    "DESCRIPTION",
    "PRICE"]
HEADER_SEC__SINGLE = [
    "SETTLEMENT DATE",
    "CUSIP",
    "QUANTITY (FAILS)",
    "PRICE"]
ROW_SEC__SOURCE = [
    "20210301",
    "G00748106",
    "STWO",
    "150425",
    "ACON S2 ACQUISITION CORP.CL A ",
    "10.40"]
ROW_SEC__SINGLE = [
    "2021-03-01",
    "G00748106",
    "150425",
    "10.40"]
ROW_SEC__MULTI = [
    "2021-03-01",
    "G00748106",
    "STWO",
    "150425",
    "ACON S2 ACQUISITION CORP.CL A ",
    "10.40"]


class TestFinraParser:
    @responses.activate
    @utils.decorators.setup_component(parsers.Finra)
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

    @utils.decorators.setup_component(parsers.Finra)
    def test_extract_ticker_from_row(self, parser, *args, **kwargs):
        row_data = ROW_FINRA__SOURCE
        assert parser.extract_ticker_from_row(row_data) == "AA"

    @utils.decorators.setup_component(parsers.Finra)
    def test_parse_row(self, parser, *args, **kwargs):
        # parser._parse_rows is set to True by the mock Settings options
        assert parser._parse_rows is True
        # Parse everything and remove the symbol.
        # used to write one symbol per file
        assert parser.parse_row(ROW_FINRA__SOURCE) == ROW_FINRA__SINGLE

        # Parse the date but keep the symbol.
        # used to write more symbols on single file
        parser._parse_rows = False
        assert parser.parse_row(ROW_FINRA__SOURCE) == ROW_FINRA__MULTI

    @utils.decorators.setup_component(parsers.Finra)
    def test_parse_headers(self, parser, *args, **kwargs):

        assert parser._parse_rows is True
        assert (
            parser.parse_headers(HEADER_FINRA__SOURCE) == HEADER_FINRA__SINGLE)
        parser._parse_rows = False
        assert (
            parser.parse_headers(HEADER_FINRA__SOURCE) == HEADER_FINRA__MULTI)

    @utils.decorators.setup_component(parsers.Finra)
    def test_get_row_date(self, parser, *args, **kwargs):
        # custom row, simulate already parsed row
        row = ["2021-04-27", "AA", "992738", "619", "2029539", "B,Q,N"]
        expected = '2021-04-27'
        parser.cache_header(HEADER_FINRA__SOURCE)
        date = parser.get_row_date(row)
        assert date == expected

        # Test with different positions
        parser._header = []
        header = ["DERP"] + HEADER_FINRA__SOURCE
        row = ["dork", "2021-04-27"] + ROW_FINRA__SOURCE[1:]
        parser.cache_header(header)
        date = parser.get_row_date(row)
        assert date == expected

        with pytest.raises(ValueError):
            parser._header = []
            parser.get_row_date(row)
        with pytest.raises(ValueError):
            parser._header = ["Not", "valid"]
            parser.get_row_date(row)

    @utils.decorators.setup_component(parsers.Finra)
    def test_data_caching(self, parser, *args, **kwargs):
        assert parser._parse_rows is True
        parser.cache_header(HEADER_FINRA__SOURCE)
        assert parser.header == HEADER_FINRA__SINGLE

        parser.cache_data("AA", ROW_FINRA__SOURCE)
        assert "AA" in parser.data
        assert parser.data["AA"] == [ROW_FINRA__SINGLE]
        # Attempt duplicating the row. should fail, based on input date
        parser.cache_data("AA", ROW_FINRA__SOURCE)
        assert len(parser.data.keys()) == 1
        # Duplicated row should not be included. matching is done with date
        assert parser.data["AA"] == [ROW_FINRA__SINGLE]

    @responses.activate
    @utils.decorators.setup_component(parsers.Finra)
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

        assert parser.header == HEADER_FINRA__SINGLE
        assert parser.data["GME"] == [['2021-04-27', '2291953', '44637', '3972777']]  # noqa


class TestSecFtdParser:

    @responses.activate
    @utils.decorators.setup_component(parsers.SecFtd)
    @utils.decorators.response_decorator(SOURCES.SEC_FTD)
    def test_process_to_csv(self, parser, response, file_num, *args, **kwargs):
        expected_rows = utils.get_expected_data_files_as_csv(
            SOURCES.SEC_FTD, file_num)
        parsed_rows = parser.process_response_to_csv(response)
        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            assert parsed_row == next(expected_rows)

    @utils.decorators.setup_component(parsers.SecFtd)
    def test_extract_ticker_from_row(self, parser, *args, **kwargs):
        assert parser.extract_ticker_from_row(ROW_SEC__SOURCE) == "STWO"

    @utils.decorators.setup_component(parsers.SecFtd)
    def test_parse_row(self, parser, *args, **kwargs):
        # SETTLEMENT DATE, CUSIP, SYMBOL, QUANTITY (FAILS), DESCRIPTION, PRICE
        row = ["20210301","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]  # noqa

        expected_multi = ["2021-03-01","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]     # noqa
        expected_single = ["2021-03-01","G00748106","150425","10.40"]    # noqa
        # parser._parse_rows is set to True by the mock Settings options
        assert parser._parse_rows is True

        # Parse everything and remove the symbol.
        # used to write one symbol per file
        assert parser.parse_row(ROW_SEC__SOURCE) == ROW_SEC__SINGLE

        # Parse the date but keep the symbol.
        # used to write more symbols on single file
        parser._parse_rows = False
        assert parser.parse_row(ROW_SEC__SOURCE) == ROW_SEC__MULTI

    @utils.decorators.setup_component(parsers.SecFtd)
    def test_parse_headers(self, parser, *args, **kwargs):
        assert parser._parse_rows is True
        assert parser.parse_headers(HEADER_SEC__SOURCE) == HEADER_SEC__SINGLE
        parser._parse_rows = False
        assert parser.parse_headers(HEADER_SEC__SOURCE) == HEADER_SEC__MULTI

    @utils.decorators.setup_component(parsers.SecFtd)
    def test_get_row_date(self, parser, *args, **kwargs):
        row = ["2021-03-01"] + ROW_SEC__SOURCE[1:]
        expected = '2021-03-01'
        parser.cache_header(HEADER_SEC__SOURCE)
        date = parser.get_row_date(row)
        assert date == expected

        # Test with different positions
        parser._header = []
        header = ["derp"] + HEADER_SEC__SOURCE
        row = ["dork", "2021-03-01"] + HEADER_SEC__SOURCE[1:]
        parser.cache_header(header)
        date = parser.get_row_date(row)
    #     assert date == expected

    @utils.decorators.setup_component(parsers.SecFtd)
    def test_data_caching(self, parser, *args, **kwargs):
        assert parser._parse_rows is True
        parser.cache_header(HEADER_SEC__SOURCE)
        assert parser.header == HEADER_SEC__SINGLE

        parser.cache_data("STWO", ROW_SEC__SOURCE)
        assert "STWO" in parser.data
        assert parser.data["STWO"] == [ROW_SEC__SINGLE]
        # Attempt duplicating the row. should fail, based on input date
        parser.cache_data("STWO", ROW_SEC__SOURCE)
        assert len(parser.data.keys()) == 1
        # Duplicated row should not be included. matching is done with date
        assert parser.data["STWO"] == [ROW_SEC__SINGLE]

    @responses.activate
    @utils.decorators.setup_component(parsers.SecFtd)
    @utils.decorators.response_decorator(SOURCES.SEC_FTD)
    def test_parse(self, parser, response, file_num, *args, **kwargs):
        expected_first_row = ['2021-03-02', '36467W109', '26373', '120.40']
        parser.settings.clear_tickers()
        for ticker in ["AMC", "GME"]:
            parser.settings.add_ticker(ticker)

        parser.parse(response)
        assert parser._parse_rows is True
        assert "GME" in parser.data.keys()
        assert "AMC" in parser.data.keys()
        assert "AA" not in parser.data.keys()
        # FIXME: This is done this way due to how the generation of the mock
        # data works. the response_decorator loops two files to pull the data
        # from, and the parser is built outside of it to iterate all files,
        # so the first time that this assert is met it counts 10 from the
        # first file and the second file adds 13.
        assert len(parser.data["GME"]) in [10, 23]
        assert expected_first_row in parser.data["GME"]
