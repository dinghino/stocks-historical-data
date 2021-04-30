import pytest
import responses
from tests import mocks, utils
from scraper.settings.constants import SOURCES

from scraper.settings import Settings
from scraper.components import parsers

def fail():
    assert True == False

class TestFinraParser:

    @responses.activate
    @utils.decorators.setup_component(parsers.Finra)
    @utils.decorators.response_decorator(SOURCES.FINRA_SHORTS)
    def test_process_to_csv(self, parser, response, file_num, *args, **kwargs):
        expected_rows = utils.get_expected_data_files_as_csv(SOURCES.FINRA_SHORTS, file_num)
        parsed_rows = parser.process_response_to_csv(response)
        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            expected_row = next(expected_rows)
            assert parsed_row == expected_row

    @utils.decorators.setup_component(parsers.Finra)
    def test_extract_ticker_from_row(self, parser, *args, **kwargs):
        # Date, Symbol, ShortVolume, ShortExemptVolume, TotalVolume, Market
        row_data = ["20210427","AA","992738","619","2029539","B,Q,N"]
        expected_output = "AA"
        assert parser.extract_ticker_from_row(row_data) == expected_output

    @utils.decorators.setup_component(parsers.Finra)
    def test_parse_row(self, parser, *args, **kwargs):
        # Date, Symbol, ShortVolume, ShortExemptVolume, TotalVolume, Market
        row = ["20210427","AA","992738","619","2029539","B,Q,N"]

        expected_multi = ["2021-04-27","AA","992738","619","2029539","B,Q,N"]
        expected_single = ["2021-04-27","992738","619","2029539"]
        # parser._parse_rows is set to True by the mock Settings options
        assert parser._parse_rows == True
        # Parse everything and remove the symbol. used to write one symbol per file
        assert parser.parse_row(row) == expected_single

        # Parse the date but keep the symbol. used to write more symbols on single file
        parser._parse_rows = False
        assert parser.parse_row(row) == expected_multi

    @utils.decorators.setup_component(parsers.Finra)
    def test_parse_headers(self, parser, *args, **kwargs):
        header = ["Date","Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"]
        expected_multi = ["Date","Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"]
        expected_single = ["Date","ShortVolume","ShortExemptVolume","TotalVolume"]

        assert parser._parse_rows == True
        assert parser.parse_headers(header) == expected_single
        parser._parse_rows = False
        assert parser.parse_headers(header) == expected_multi

    @utils.decorators.setup_component(parsers.Finra)
    def test_get_row_date(self, parser, *args, **kwargs):
        header = ["Date","Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"]
        row = ["2021-04-27","AA","992738","619","2029539","B,Q,N"]
        expected = '2021-04-27'
        parser.cache_header(header)
        date = parser.get_row_date(row)
        assert date == expected

        # Test with different positions
        parser._header = []
        header = ["DERP", "Date","Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"]
        row = ["dork", "2021-04-27","AA","992738","619","2029539","B,Q,N"]
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
        header = ["Date","Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"]
        expected_header_single = ["Date","ShortVolume","ShortExemptVolume","TotalVolume"]
        expected_header_multi = ["Date","Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"]

        row = ["20210427","AA","992738","619","2029539","B,Q,N"]
        expected_row_single = ["2021-04-27","992738","619","2029539"]
        expected_row_multi = ["2021-04-27","AA","992738","619","2029539","B,Q,N"]

        assert parser._parse_rows == True
        parser.cache_header(header)
        assert parser.header == expected_header_single

        parser.cache_data("AA", row)
        assert "AA" in parser.data
        assert parser.data["AA"] == [expected_row_single]
        # Attempt duplicating the row. should fail, based on input date
        parser.cache_data("AA", row)
        assert len(parser.data.keys()) == 1
        # Duplicated row should not be included. matching is done with date
        assert parser.data["AA"] == [expected_row_single]

    @responses.activate
    @utils.decorators.setup_component(parsers.Finra)
    @utils.decorators.response_decorator(SOURCES.FINRA_SHORTS)
    def test_parse(self, parser, response, file_num, *args, **kwargs):
        expected_header = ["Date","ShortVolume","ShortExemptVolume","TotalVolume"]

        parser.settings.clear_tickers()
        for ticker in ["AMC", "GME"]:
            parser.settings.add_ticker(ticker)

        parser.parse(response)
        assert parser._parse_rows == True
        assert "GME" in parser.data.keys()
        assert "AMC" in parser.data.keys()
        assert "AA" not in parser.data.keys()
        
        assert parser.data["GME"] == [ ['2021-04-27', '2291953', '44637', '3972777'] ]


class TestSecFtdParser:

    @responses.activate
    @utils.decorators.setup_component(parsers.SecFtd)
    @utils.decorators.response_decorator(SOURCES.SEC_FTD)
    def test_process_to_csv(self, parser, response, file_num, *args, **kwargs):
        expected_rows = utils.get_expected_data_files_as_csv(SOURCES.SEC_FTD, file_num)
        parsed_rows = parser.process_response_to_csv(response)
        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            assert parsed_row == next(expected_rows)

    @utils.decorators.setup_component(parsers.SecFtd)    
    def test_extract_ticker_from_row(self, parser, *args, **kwargs):
        # SETTLEMENT DATE, CUSIP, SYMBOL, QUANTITY (FAILS), DESCRIPTION, PRICE
        row_data = ["20210301","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]
        expected_output = "STWO"
        assert parser.extract_ticker_from_row(row_data) == expected_output

    @utils.decorators.setup_component(parsers.SecFtd)
    def test_parse_row(self, parser, *args, **kwargs):
        # SETTLEMENT DATE, CUSIP, SYMBOL, QUANTITY (FAILS), DESCRIPTION, PRICE
        row = ["20210301","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]

        expected_multi = ["2021-03-01","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]
        expected_single = ["2021-03-01","G00748106","150425","10.40"]
        # parser._parse_rows is set to True by the mock Settings options
        assert parser._parse_rows == True

        # Parse everything and remove the symbol. used to write one symbol per file
        out = parser.parse_row(row)
        assert out == expected_single

        # Parse the date but keep the symbol. used to write more symbols on single file
        parser._parse_rows = False
        out = parser.parse_row(row)
        assert out == expected_multi

    @utils.decorators.setup_component(parsers.SecFtd)
    def test_parse_headers(self, parser, *args, **kwargs):
        header = ["SETTLEMENT DATE","CUSIP","SYMBOL","QUANTITY (FAILS)","DESCRIPTION","PRICE"]
        expected_multi = ["SETTLEMENT DATE","CUSIP","SYMBOL","QUANTITY (FAILS)","DESCRIPTION","PRICE"]
        expected_single = ["SETTLEMENT DATE","CUSIP","QUANTITY (FAILS)","PRICE"]

        assert parser._parse_rows == True
        assert parser.parse_headers(header) == expected_single
        parser._parse_rows = False
        assert parser.parse_headers(header) == expected_multi
    
    @utils.decorators.setup_component(parsers.SecFtd)
    def test_get_row_date(self, parser, *args, **kwargs):
        header = ["SETTLEMENT DATE","CUSIP","SYMBOL","QUANTITY (FAILS)","DESCRIPTION","PRICE"]
        row = ["2021-03-01","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]
        expected = '2021-03-01'
        parser.cache_header(header)
        date = parser.get_row_date(row)
        assert date == expected

        # Test with different positions
        parser._header = []
        header = ["derp","SETTLEMENT DATE","CUSIP","SYMBOL","QUANTITY (FAILS)","DESCRIPTION","PRICE"]
        row = ["dork","2021-03-01","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]
        parser.cache_header(header)
        date = parser.get_row_date(row)
    #     assert date == expected

    @utils.decorators.setup_component(parsers.SecFtd)
    def test_data_caching(self, parser, *args, **kwargs):
        header = ["SETTLEMENT DATE","CUSIP","SYMBOL","QUANTITY (FAILS)","DESCRIPTION","PRICE"]
        expected_header_multi = ["SETTLEMENT DATE","CUSIP","SYMBOL","QUANTITY (FAILS)","DESCRIPTION","PRICE"]
        expected_header_single = ["SETTLEMENT DATE","CUSIP","QUANTITY (FAILS)","PRICE"]

        row = ["20210301","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]
        expected_row_multi = ["2021-03-01","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]
        expected_row_single = ["2021-03-01","G00748106","150425","10.40"]

        assert parser._parse_rows == True
        parser.cache_header(header)
        assert parser.header == expected_header_single

        parser.cache_data("STWO", row)
        assert "STWO" in parser.data
        assert parser.data["STWO"] == [expected_row_single]
        # Attempt duplicating the row. should fail, based on input date
        parser.cache_data("STWO", row)
        assert len(parser.data.keys()) == 1
        # Duplicated row should not be included. matching is done with date
        assert parser.data["STWO"] == [expected_row_single]

    @responses.activate
    @utils.decorators.setup_component(parsers.SecFtd)
    @utils.decorators.response_decorator(SOURCES.SEC_FTD)
    def test_parse(self, parser, response, file_num, *args, **kwargs):
        expected_header = ["SETTLEMENT DATE","CUSIP","QUANTITY (FAILS)","PRICE"]
        expected_first_row = ['2021-03-02', '36467W109', '26373', '120.40']
        parser.settings.clear_tickers()
        for ticker in ["AMC", "GME"]:
            parser.settings.add_ticker(ticker)

        parser.parse(response)
        assert parser._parse_rows == True
        assert "GME" in parser.data.keys()
        assert "AMC" in parser.data.keys()
        assert "AA" not in parser.data.keys()
        # FIXME: This is done this way due to how the generation of the mock data
        # works. the response_decorator loops two files to pull the data from,
        # and the parser is built outside of it to iterate all files,
        # so the first time that this assert is met it counts 10 from the first file
        # and the second file adds 13.
        assert len(parser.data["GME"]) in [10, 23]
        assert expected_first_row in parser.data["GME"]
