import codecs, csv
from scraper.components.parsers.base_parser import Parser

class FinraParser(Parser):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def process_response_to_csv(self, response):
        return csv.reader(codecs.iterdecode(response.iter_lines(), 'utf-8'))

    def extract_ticker_from_row(self, row_data):
        return row_data[1]

    def parse_headers(self, data):
        if not self._parse_rows:
            return data
        return ["Date"] + data[2:5]
    
    def parse_row(self, row):
        date = self.parse_date(row[0])
        # source data is 
        # date | ticker | short volume | short exempt volume | total volume | market
        if not self._parse_rows:
            return [date] + row[1:]
        return [date] + row[2:5]
