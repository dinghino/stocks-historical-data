from scraper.components.parsers.base_parser import Parser

class FinraParser(Parser):
    def __init__(self, strip_ticker=True):
        super().__init__()

        self._strip_ticker = strip_ticker

    def parse(self, row, tickers):
        data = row[0].split("|")

        if len(data) <=1:
            return

        ticker = data[1]
        # if no tickers list is provided we want all the things.
        # otherwise check if the current row ticker is in our list
        if len(tickers) == 0 or ticker in tickers:
            self.cache_data(ticker, self._parse_row(data))    
    
    def cache_data(self, ticker, data):
        # first time we encouter this ticker. create the list and prepend the header
        # that we can later strip if we want a big old file with everything
        if ticker not in self._cache:
            self._cache[ticker] = []
            self._cache[ticker].append(self.header)

        self._cache[ticker].append(data)
    
    def cache_header(self, header):
        # cache the header for the dataset to be used later
        if len(self.header) is 0:
            _header = header[0].split("|")
            self._header = self._parse_headers(_header)
    
    def _parse_headers(self, data):
        if not self._strip_ticker:
            return data
        return ["Date"] + data[2:5]
    
    def _parse_row(self, row):
        date = self._parse_date(row[0])
        # source data is 
        # date | ticker | short volume | short exempt volume | total volume | market
        if not self._strip_ticker:
            return [date] + row[1:]
        return [date] + row[2:5]
