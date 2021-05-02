import csv
import codecs
from stonks.constants import SOURCES
from stonks.components.parsers.base_parser import Parser


class FinraParser(Parser):

    @staticmethod
    def is_for():
        return SOURCES.FINRA_SHORTS

    def process_response_to_csv(self, response):
        return csv.reader(
            codecs.iterdecode(
                response.iter_lines(), 'utf-8', errors="replace"))

    def extract_ticker_from_row(self, row_data):
        return row_data[1]

    def parse_headers(self, header):
        out = list(header)

        if not self._parse_rows:
            return out
        out.remove("Symbol")
        out.remove("Market")
        return out

    def parse_row(self, row):
        date = self.parse_date(row[0])
        out = list(row)
        out[0] = date
        # source data is
        # date | ticker | short volume | short exempt volume | total volume | market # noqa
        if not self._parse_rows:
            return out
        # remove symbol
        out.remove(out[1])
        # date | short volume | short exempt volume | total volume | market
        out.remove(out[-1])
        # date | short volume | short exempt volume | total volume
        return out
