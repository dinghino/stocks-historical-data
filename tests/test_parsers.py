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
    @utils.setup_parser(parsers.Finra)
    @utils.response_decorator(SOURCES.FINRA_SHORTS)
    def test_process_to_csv(self, parser, response, file_num):
        expected_rows = utils.get_expected_data_files_as_csv(SOURCES.FINRA_SHORTS, file_num)
        parsed_rows = parser.process_response_to_csv(response)
        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            expected_row = next(expected_rows)
            assert parsed_row == expected_row

    @utils.setup_parser(parsers.Finra)
    def test_extract_ticker_from_row(self, parser):
        # Date, Symbol, ShortVolume, ShortExemptVolume, TotalVolume, Market
        row_data = ["20210427","AA","992738","619","2029539","B,Q,N"]
        expected_output = "AA"
        assert parser.extract_ticker_from_row(row_data) == expected_output

    @utils.setup_parser(parsers.Finra)
    def test_parse_row(self, parser):
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

    @utils.setup_parser(parsers.Finra)
    def test_parse_headers(self, parser):
        header = ["Date","Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"]
        expected_multi = ["Date","Symbol","ShortVolume","ShortExemptVolume","TotalVolume","Market"]
        expected_single = ["Date","ShortVolume","ShortExemptVolume","TotalVolume"]

        assert parser._parse_rows == True
        assert parser.parse_headers(header) == expected_single
        parser._parse_rows = False
        assert parser.parse_headers(header) == expected_multi


class TestSecFtdParser:

    @responses.activate
    @utils.setup_parser(parsers.SecFtd)
    @utils.response_decorator(SOURCES.SEC_FTD)
    def test_process_to_csv(self, parser, response, file_num):
        expected_rows = utils.get_expected_data_files_as_csv(SOURCES.SEC_FTD, file_num)
        parsed_rows = parser.process_response_to_csv(response)
        # Check that we got the same number of rows
        assert len(list(expected_rows)) == len(list(parsed_rows))
        for parsed_row in parsed_rows:
            assert parsed_row == next(expected_rows)

    @utils.setup_parser(parsers.SecFtd)    
    def test_extract_ticker_from_row(self, parser):
        # SETTLEMENT DATE, CUSIP, SYMBOL, QUANTITY (FAILS), DESCRIPTION, PRICE
        row_data = ["20210301","G00748106","STWO","150425","ACON S2 ACQUISITION CORP.CL A ","10.40"]
        expected_output = "STWO"
        assert parser.extract_ticker_from_row(row_data) == expected_output

    @utils.setup_parser(parsers.SecFtd)
    def test_parse_row(self, parser):
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

    @utils.setup_parser(parsers.SecFtd)
    def test_parse_headers(self, parser):
        header = ["SETTLEMENT DATE","CUSIP","SYMBOL","QUANTITY (FAILS)","DESCRIPTION","PRICE"]
        expected_multi = ["SETTLEMENT DATE","CUSIP","SYMBOL","QUANTITY (FAILS)","DESCRIPTION","PRICE"]
        expected_single = ["SETTLEMENT DATE","CUSIP","QUANTITY (FAILS)","PRICE"]

        assert parser._parse_rows == True
        assert parser.parse_headers(header) == expected_single
        parser._parse_rows = False
        assert parser.parse_headers(header) == expected_multi
