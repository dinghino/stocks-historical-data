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
    def __init__(self, settings, debug=False):
        # def __init__(self, parse_rows, debug=False):
        self._cache = {}
        self._header = []
        self.settings = settings
        self._parse_rows = settings.output_type == settings.OUTPUT_TYPE.SINGLE_TICKER
        # self._parse_rows = parse_rows
        self.debug = debug

    @property
    def header(self):
        return self._header
    @property
    def data(self):
        return self._cache

    def parse_date(self, datestr):
        """ Takes a %Y%m%d formatted date and outputs it to "%Y-%m-%d" """
        return dt.strptime(datestr, "%Y%m%d").strftime("%Y-%m-%d")

    @abc.abstractmethod
    def process_response_to_csv(self, response):
        """
        Takes the response object from a performed requests call and should
        return a csv.reader object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def extract_ticker_from_row(self, row_data):
        """
        Get the ticker from the right column of the row.
        Mainly used to filter out rows
        """
        raise NotImplementedError

    @abc.abstractmethod
    def parse_row(self, row):
        raise NotImplementedError

    def parse(self, response, separator='|'):
        reader = self.process_response_to_csv(response)

        # first line is the header. cache it
        self.cache_header(next(reader))

        for row in reader:
            data = row[0].split(separator)
            if len(data) <= 1:
                continue

            ticker = self.extract_ticker_from_row(data)
            if len(self.settings.tickers) == 0 or ticker in self.settings.tickers:
                self.cache_data(ticker, data)

    def cache_data(self, ticker, row):
        # first time we encouter this ticker. create the list and prepend the header
        # that we can later strip if we want a big old file with everything
        if ticker not in self._cache:
            self._cache[ticker] = []
            self._cache[ticker].append(self.header)
    
        self._cache[ticker].append(self.parse_row(row))
    
    def cache_header(self, header, separator="|"):
        # cache the header for the dataset to be used later
        if len(self.header) is 0:
            _header = header[0].split(separator)
            self._header = self.parse_headers(_header)
