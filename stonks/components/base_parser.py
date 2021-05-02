import abc
from stonks.components.component_base import ComponentBase
from datetime import datetime as dt

# To be compatible with writers cache structure should be a dictionary shaped
# as { [TICKER]: [CSV ROWS] } and be available in self._cache
# The header of the CSV should be extracted and kept in the separate
# self._header property to be used as needed.
# Remember to parse the columns in the same order for both headers and columns
# And, if available, to parse the date in an interpretable format from other
# applications (for example Excel) using the provided method


class ParserBase(ComponentBase):
    def __init__(self, settings, debug=False):
        ComponentBase.__init__(self)

        self._cache = {}
        self._header = []
        self.settings = settings
        self._parse_rows = (
            settings.output_type == settings.OUTPUT_TYPE.SINGLE_TICKER)
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
    def process_response_to_csv(self, response):  # pragma: no cover
        """
        Takes the response object from a performed requests call and should
        return a csv.reader object
        """
        return NotImplemented

    @abc.abstractmethod
    def extract_ticker_from_row(self, row_data):  # pragma: no cover
        """
        Get the ticker from the right column of the row.
        Mainly used to filter out rows
        """
        return NotImplemented

    @abc.abstractmethod
    def parse_row(self, row):  # pragma: no cover
        return NotImplemented

    def parse(self, response, separator='|'):
        reader = self.process_response_to_csv(response)

        # first line is the header. cache it
        self.cache_header(next(reader)[0].split(separator))

        for row in reader:
            data = row[0].split(separator)
            if len(data) <= 1:
                continue

            tickers = self.settings.tickers
            ticker = self.extract_ticker_from_row(data)

            if len(self.settings.tickers) == 0 or ticker in tickers:
                self.cache_data(ticker, data)

    def cache_data(self, ticker, row):
        # first time we encouter this ticker. create the list and prepend the
        # header that we can later strip if we want a big old file with
        # everything
        if ticker not in self._cache:
            self._cache[ticker] = []

        # Avoid duplicating rows. This is done
        parsed = self.parse_row(row)
        if not self.row_already_stored(ticker, parsed):
            self._cache[ticker].append(parsed)

    def cache_header(self, header):
        # cache the header for the dataset to be used later
        if len(self.header) == 0:
            self._header = self.parse_headers(header)

    def row_already_stored(self, ticker, row):
        return row in self.data[ticker]

    def get_row_date(self, row):
        """Get the date from a row of data regardless of its position.
        Use the headers to find the column.
        Obviously ate header should contain the word 'date' in it"""
        index = None
        if len(self.header) == 0:
            # TODO: Better exception!
            raise ValueError("An header must be cached as first thing")
        # Note: we expect the date to be in the first column, always

        for col in self.header:
            if "DATE" in col.upper():
                index = self.header.index(col)
        if index is None:
            raise ValueError("Date column not found")

        return row[index]
