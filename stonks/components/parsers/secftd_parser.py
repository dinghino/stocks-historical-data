from io import BytesIO
import csv
import codecs
from zipfile import ZipFile

from stonks.constants import SOURCES
from stonks.components.base_parser import Parser


class SecFtdParser(Parser):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    @staticmethod
    def is_for():
        return SOURCES.SEC_FTD

    def process_response_to_csv(self, response):
        zf = ZipFile(BytesIO(response.content), 'r')
        # Zip should contain only one file
        filename = zf.namelist()[0]

        if not filename:    # pragma: no cover
            raise ValueError("Zip was missing the content!")

        return csv.reader(
            codecs.iterdecode(zf.open(filename), 'utf-8', errors="replace"))

    def extract_ticker_from_row(self, row_data):
        return row_data[2]

    def parse_headers(self, header):
        if not self._parse_rows:
            return header

        out = list(header)
        out.remove("SYMBOL")
        out.remove("DESCRIPTION")
        return out

    def parse_row(self, row):
        date = self.parse_date(row[0])
        # SETTLEMENT DATE |CUSIP | SYMBOL | QUANTITY (FAILS) | DESCRIPTION | PRICE  # noqa
        out = list(row)
        out[0] = date
        if not self._parse_rows:
            return out
        # remove symbol
        out.remove(out[2])
        # SETTLEMENT DATE |CUSIP | QUANTITY (FAILS) | DESCRIPTION | PRICE
        # remove description. out[4-1]
        out.remove(out[3])
        # SETTLEMENT DATE |CUSIP | QUANTITY (FAILS) | PRICE
        return out
