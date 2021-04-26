from io import BytesIO
import codecs, csv
from zipfile import ZipFile

from scraper.components.parsers.base_parser import Parser

class SecFtdParser(Parser):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def process_response_to_csv(self, response):
        zf = ZipFile(BytesIO(response.content), 'r')
        # Zip should contain only one file
        filename = zf.namelist()[0]
        if not filename:
            raise ValueError("Zip was missing the content!")

        return csv.reader(codecs.iterdecode(zf.open(filename), 'utf-8'))

    def extract_ticker_from_row(self, row_data):
        return row_data[2]

    def parse_headers(self, header):
        if not self._parse_rows:
            return header
        header.remove("SYMBOL")
        return header
    
    def parse_row(self, row):
        date = self.parse_date(row[0])
        # source data is 
        # SETTLEMENT DATE |CUSIP | SYMBOL | QUANTITY (FAILS) | DESCRIPTION | PRICE
        if not self._parse_rows:
            return [date] + row[1:]
        print(row)
        return [date, row[1]] + row[3:]
