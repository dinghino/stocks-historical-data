import abc
from datetime import datetime as dt

# To be compatible with writers cache structure should be a dictionary shaped as
# { [TICKER]: [CSV ROWS] } and be available in self._cache
# The header of the CSV should be extracted and kept in the separate self._header
# property to be used as needed.
# Remember to parse the columns in the same order for both headers and columns
# And, if available, to parse the date in an interpretable format from other
# applications (for example Excel) using the provided method

class Parser(abc.ABC):
    def __init__(self, parse_rows, debug=False):
        self._cache = {}
        self._header = []
        self._parse_rows = parse_rows
        self.debug = debug

    @property
    def header(self):
        return self._header
    @property
    def data(self):
        return self._cache

    def parse_date(self, datestr):
        return dt.strptime(datestr, "%Y%m%d").strftime("%Y-%m-%d")

    @abc.abstractmethod
    def parse_headers(self, data):
        return data

    def cache_data(self, ticker, data):
        # first time we encouter this ticker. create the list and prepend the header
        # that we can later strip if we want a big old file with everything
        if ticker not in self._cache:
            self._cache[ticker] = []
            self._cache[ticker].append(self.header)
    
        self._cache[ticker].append(data)
    
    def cache_header(self, header, separator="|"):
        # cache the header for the dataset to be used later
        if len(self.header) is 0:
            _header = header[0].split(separator)
            self._header = self.parse_headers(_header)

    @abc.abstractmethod
    def parse(self, row, tickers):
        raise NotImplementedError
