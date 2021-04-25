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
    def __init__(self):
        self._cache = {}
        self._header = []

    @property
    def header(self):
        return self._header
    @property
    def data(self):
        return self._cache

    def _parse_date(self, datestr):
        return dt.strptime(datestr, "%Y%m%d").strftime("%Y-%m-%d")

    @abc.abstractmethod
    def parse(self, row, tickers):
        raise NotImplementedError

