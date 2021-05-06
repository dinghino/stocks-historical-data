import os
from pathlib import Path
import json
import bisect
import datetime

# this is strange. if this import is missing hell breaks lose.

from stonks import exceptions, utils
from stonks.constants import FIELDS, VALID_DATES_FORMAT
from stonks.components import manager
from stonks.definitions import DEFAULT_SETTINGS_PATH, DEFAULT_OUTPUT_PATH


class Settings:

    # Reference for all the string that will be used in the settings file
    # for each field.
    FIELDS = FIELDS
    # Reference to quickly access all valid formats for dates.
    VALID_DATES_FORMAT = VALID_DATES_FORMAT
    # Default path for the settings to be saved to or loaded from.
    # This applies if no other path is provided either on creation or when
    # calling init.
    settings_path = DEFAULT_SETTINGS_PATH
    # Default path to output the data if nothing else is provided.
    default_output_path = DEFAULT_OUTPUT_PATH
    # default csv dialect is excel, so we default to that in case it's missing
    default_dialect = 'excel'

    default_start_date = None
    default_end_date = None
    default_tickers = []
    default_sources = []
    default_out_type = None

    def __init__(self, settings_path=None, debug=False):
        self.debug = debug

        self.reset()

        if (settings_path):  # pragma: no cover
            self.settings_path = settings_path
        else:
            self.settings_path = DEFAULT_SETTINGS_PATH

    def init(self, path=None):
        self.errors = []

        if not manager.get_sources():
            raise exceptions.MissingSourceHandlersException

        if not manager.get_outputs():
            raise exceptions.MissingWritersException

        if not path:
            path = self.settings_path

        try:
            self.from_file(path)
        except exceptions.MissingFile:
            try:
                self.from_file(self.settings_path)
            except exceptions.MissingFile:
                pass
        except exceptions.FileReadError:  # pragma: no cover
            pass
        except Exception as e:  # pragma: no cover
            self._add_err(str(e))
            raise e

        self.init_done = True
        return self.init_done

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, date):
        self._start_date = self._parse_datestr(date, 'start date')

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, date):
        self._end_date = self._parse_datestr(date, 'end date')

    def _parse_datestr(self, datestr, field_name):
        for frmt in VALID_DATES_FORMAT:
            try:
                return datetime.datetime.strptime(datestr, frmt).date()
            except ValueError:
                pass

        raise exceptions.DateException(datestr, field_name)

    @property
    def tickers(self):
        return self._tickers

    def add_ticker(self, ticker):
        ticker = ticker.upper()
        if (ticker in self._tickers):
            return
        try:
            bisect.insort(self._tickers, ticker)
        except Exception:  # pragma: no cover
            pass

    def remove_ticker(self, ticker):
        try:
            self._tickers.remove(ticker.upper())
        except ValueError:
            pass

    def clear_tickers(self):
        self._tickers = []

    @property
    def output_type(self):
        return self._out_type

    @output_type.setter
    def output_type(self, value):
        if manager.validate_output(value):
            self._out_type = value

    @property
    def output_path(self):
        return self._out_path

    @output_path.setter
    def output_path(self, path):
        # check if path ends with .csv
        # if that's the case, the requested output has the filename in it
        if utils.path_contains_filename(path):
            self.path_with_filename = True
            self._out_path = path
            return

        # otherwise that's just the folder we want to put the file
        # (naming will be done before writing).
        self.path_with_filename = False
        self._out_path = path

    @property
    def sources(self):
        return self._sources

    def add_source(self, source):
        # Throws SourceException if fails
        if manager.validate_source(source) and source not in self.sources:
            bisect.insort(self._sources, source)

    def remove_source(self, source):
        # Try to remove the given source. we don't care if it fails
        # and if using the cli it should never happen
        try:
            self._sources.remove(source)
        except ValueError:  # pragma: no cover
            pass

    @property
    def csv_out_dialect(self):
        return self._csv_out_dialect

    @csv_out_dialect.setter
    def csv_out_dialect(self, value):
        if manager.validate_dialect(value):
            self._csv_out_dialect = value

    def _read_options_file(self, path):
        # Try to open the given path and read the json data in it.
        # Catch the FileNotFound from `open` and raise custom exception
        # if needed also handle the file read error
        try:
            with open(path) as file:
                data = json.loads(file.read())
        except FileNotFoundError:
            my_exception = exceptions.MissingFile(path)
            self._add_err(str(my_exception))
            self.settings_loaded = False
            raise my_exception
        # catch everything else, especially json read errors
        except json.JSONDecodeError:  # pragma: no cover
            my_exception = exceptions.FileReadError(path)
            self._add_err(str(my_exception))
            self.settings_loaded = False
            raise my_exception

        return data

    def from_file(self, path):
        data = self._read_options_file(path)

        def is_set(field_name):
            exists = field_name in data and data[field_name] is not None
            if exists and type(data[field_name]) not in [int, float]:
                exists = exists and len(data[field_name]) > 0
            return exists

        if is_set(FIELDS.START):
            self.start_date = data[FIELDS.START]
        if is_set(FIELDS.END):
            self.end_date = data[FIELDS.END]
        if is_set(FIELDS.SETTINGS_PATH):
            self.settings_path = data[FIELDS.SETTINGS_PATH]
        if is_set(FIELDS.TICKERS):
            self._tickers = data[FIELDS.TICKERS]
        if is_set(FIELDS.PATH):
            self.output_path = data[FIELDS.PATH]
        else:  # pragma: no cover - can't be tested for default path
            self.output_path = self.default_output_path

        if is_set(FIELDS.TYPE):
            try:
                self.output_type = data[FIELDS.TYPE]
            except exceptions.OutputTypeException as e:  # pragma: no cover
                self._add_err(str(e))
                self._output_type = None

        if is_set(FIELDS.SOURCES):
            for source in data[FIELDS.SOURCES]:
                try:
                    self.add_source(source)
                except exceptions.SourceException as e:  # pragma: no cover
                    self._add_err(str(e))

        if is_set(FIELDS.CSV_DIALECT):
            try:
                self.csv_out_dialect = data[FIELDS.CSV_DIALECT]
            except exceptions.DialectException:  # pragma: no cover
                self.csv_out_dialect = Settings.default_dialect

        self.settings_loaded = True
        return self.settings_loaded

    def serialize(self):
        data = {}
        if self.start_date is not None:
            data[FIELDS.START] = self.start_date.strftime("%Y-%m-%d")
        else:  # pragma: no cover
            data[FIELDS.START] = None
        if self.end_date is not None:
            data[FIELDS.END] = self.end_date.strftime("%Y-%m-%d")
        else:  # pragma: no cover
            data[FIELDS.END] = None

        data[FIELDS.TYPE] = self.output_type
        data[FIELDS.PATH] = (
            self.output_path or self.default_output_path)
        data[FIELDS.TICKERS] = self.tickers
        data[FIELDS.SOURCES] = self._sources
        data[FIELDS.CSV_DIALECT] = self.csv_out_dialect
        data[FIELDS.SETTINGS_PATH] = (
            self.settings_path or self.__default_settings_path)

        return data

    def to_file(self, path=None):
        if not path:  # pragma: no cover
            path = self.settings_path

        base, fname = os.path.split(os.path.abspath(path))

        if not os.path.exists(path):  # pragma: no cover
            Path(base).mkdir(parents=True, exist_ok=True)

        try:
            with open(os.path.join(base, fname), "w") as file:
                file.write(json.dumps(self.serialize(), indent=2))

        except Exception as e:  # pragma: no cover
            self._add_err(str(e))
            return False
        return True

    def _add_err(self, err):
        self.errors.append(err)

    def reset(self):
        self._start_date = Settings.default_start_date
        self._end_date = Settings.default_end_date
        self._tickers = Settings.default_tickers
        self._sources = Settings.default_sources
        self._out_type = Settings.default_out_type
        self._out_path = Settings.default_output_path
        self._csv_out_dialect = Settings.default_dialect
        self.parse_rows = False
        # if the provided path to output contains the filename too.
        # Should default to False
        self.path_with_filename = utils.path_contains_filename(
            Settings.default_output_path)

        self.settings_loaded = False
        self.init_done = False

        self.errors = []
