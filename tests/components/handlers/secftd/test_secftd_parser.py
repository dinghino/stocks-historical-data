import responses
from tests import utils
from stonks.components.handlers import secftd

HEADER_SOURCE = [
    "SETTLEMENT DATE",
    "CUSIP",
    "SYMBOL",
    "QUANTITY (FAILS)",
    "DESCRIPTION",
    "PRICE"]
HEADER_MULTI = [
    "SETTLEMENT DATE",
    "CUSIP",
    "SYMBOL",
    "QUANTITY (FAILS)",
    "DESCRIPTION",
    "PRICE"]
HEADER_SINGLE = [
    "SETTLEMENT DATE",
    "CUSIP",
    "QUANTITY (FAILS)",
    "PRICE"]
ROW_SOURCE = [
    "20210301",
    "G00748106",
    "STWO",
    "150425",
    "ACON S2 ACQUISITION CORP.CL A ",
    "10.40"]
ROW_SINGLE = [
    "2021-03-01",
    "G00748106",
    "150425",
    "10.40"]
ROW_MULTI = [
    "2021-03-01",
    "G00748106",
    "STWO",
    "150425",
    "ACON S2 ACQUISITION CORP.CL A ",
    "10.40"]


class TestSecFtdParser:
    @responses.activate
    @utils.decorators.register_components
    @utils.decorators.setup_component(secftd.Parser)
    @utils.decorators.response_decorator(secftd.source)
    def test_process_to_csv(self, parser, response, file_num, *args, **kwargs):
        expected_rows = utils.get_expected_data_files_as_csv(
            secftd.source, file_num)
        parsed_rows = parser.process_response_to_csv(response)
        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            assert parsed_row == next(expected_rows)

    @utils.decorators.register_components
    @utils.decorators.setup_component(secftd.Parser)
    def test_extract_ticker_from_row(self, parser, *args, **kwargs):
        assert parser.extract_ticker_from_row(ROW_SOURCE) == "STWO"

    @utils.decorators.register_components
    @utils.decorators.setup_component(secftd.Parser)
    def test_parse_row(self, parser, *args, **kwargs):
        # parser._parse_rows is set to True by the mock Settings options
        parser._parse_rows = True
        # Parse everything and remove the symbol.
        # used to write one symbol per file
        assert parser.parse_row(ROW_SOURCE) == ROW_SINGLE

        # Parse the date but keep the symbol.
        # used to write more symbols on single file
        parser._parse_rows = False
        assert parser.parse_row(ROW_SOURCE) == ROW_MULTI

    @utils.decorators.register_components
    @utils.decorators.setup_component(secftd.Parser)
    def test_parse_headers(self, parser, *args, **kwargs):
        parser._parse_rows = True
        assert parser.parse_headers(HEADER_SOURCE) == HEADER_SINGLE
        parser._parse_rows = False
        assert parser.parse_headers(HEADER_SOURCE) == HEADER_MULTI

    @utils.decorators.register_components
    @utils.decorators.setup_component(secftd.Parser)
    def test_get_row_date(self, parser, *args, **kwargs):
        row = ["2021-03-01"] + ROW_SOURCE[1:]
        expected = '2021-03-01'
        parser.cache_header(HEADER_SOURCE)
        date = parser.get_row_date(row)
        assert date == expected

        # Test with different positions
        parser._header = []
        header = ["derp"] + HEADER_SOURCE
        row = ["dork", "2021-03-01"] + HEADER_SOURCE[1:]
        parser.cache_header(header)
        date = parser.get_row_date(row)
    #     assert date == expected

    @utils.decorators.register_components
    @utils.decorators.setup_component(secftd.Parser)
    def test_data_caching(self, parser, *args, **kwargs):
        parser._parse_rows = True
        parser.cache_header(HEADER_SOURCE)
        assert parser.header == HEADER_SINGLE

        parser.cache_data("STWO", ROW_SOURCE)
        assert "STWO" in parser.data
        assert parser.data["STWO"] == [ROW_SINGLE]
        # Attempt duplicating the row. should fail, based on input date
        parser.cache_data("STWO", ROW_SOURCE)
        assert len(parser.data.keys()) == 1
        # Duplicated row should not be included. matching is done with date
        assert parser.data["STWO"] == [ROW_SINGLE]

    @responses.activate
    @utils.decorators.register_components
    @utils.decorators.setup_component(secftd.Parser)
    @utils.decorators.response_decorator(secftd.source)
    def test_parse(self, parser, response, file_num, *args, **kwargs):
        expected_first_row = ['2021-03-02', '36467W109', '26373', '120.40']
        parser._parse_rows = True
        parser.settings.clear_tickers()
        for ticker in ["AMC", "GME"]:
            parser.settings.add_ticker(ticker)

        parser.parse(response)
        assert parser._parse_rows is True
        assert "GME" in parser.data.keys()
        assert "AMC" in parser.data.keys()
        assert "AA" not in parser.data.keys()
        # This is done this way due to how the generation of the mock
        # data works. the response_decorator loops two files to pull the data
        # from, and the parser is built outside of it to iterate all files,
        # so the first time that this assert is met it counts 10 from the
        # first file and the second file adds 13.
        assert len(parser.data["GME"]) in [10, 23]
        assert expected_first_row in parser.data["GME"]
