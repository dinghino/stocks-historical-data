import os
import time
import json
import bisect
import datetime

import click

from scraper import utils

from scraper.settings import exceptions
from scraper.settings import constants

class Settings:

    # Constants
    FIELDS = constants.FIELDS
    OUTPUT_TYPE = constants.OUTPUT_TYPE
    SOURCES = constants.SOURCES
    CSV_OUT_DIALECTS = constants.CSV_OUT_DIALECTS
    VALID_DATES_FORMAT = constants.VALID_DATES_FORMAT

    # Exceptions
    DateException = exceptions.DateException
    OutputTypeException = exceptions.OutputTypeException
    SourceException = exceptions.SourceException
    MissingFile = exceptions.MissingFile

    # Default settings for paths
    settings_path = './data/options.json'
    default_output_path = './data/output/'

    def __init__(self, settings_path=None):
        self._start_date = None
        self._end_date = None
        self._tickers = []
        self._sources = []
        self._out_type = constants.OUTPUT_TYPE.SINGLE_TICKER
        self._out_path = self.default_output_path
        self._csv_out_dialect = constants.CSV_OUT_DIALECTS.DEFAULT

        self.debug = False
        self.path_with_filename = False
        
        if (settings_path):
            self.settings_path = settings_path

        self.settings_loaded = False
        self.init_done = False

        self.errors = []

    def init(self, path=None):
        self.errors = []

        if not path:
            path = self.settings_path
        
        # if not path:
        #     self.init_done = True
        #     # NOTE: This should never trigger since we have defaults
        #     self._add_err("Init could not find a path to set the options")
        #     return self.init_done

        try:
            self.from_file(path)
        except exceptions.MissingFile:
            try:
                self.from_file(self.settings_path)
            except exceptions.MissingFile:
                pass
        except Exception as e:
            self._add_err(str(e))
            raise e
        finally:
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
        for frmt in constants.VALID_DATES_FORMAT:
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
        except:
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
        if constants.OUTPUT_TYPE.validate(value):
            self._out_type = value

    @property
    def output_path(self):
        return self._out_path

    @output_path.setter
    def output_path(self, path):
        # check if path ends with .csv
        # if that's the case, the requested output has the filename in it
        if path[-4:] == '.csv':
            self.path_with_filename = True
            self._out_path = path
            return

        # otherwise that's just the folder we want to put the file (naming will be
        # done before writing), so check for trailing slash and add it if missing
        self.path_with_filename = False
        if path[-1] is not '/':
            path += '/'

        self._out_path = path

    @property
    def sources(self):
        return self._sources

    def add_source(self, source):
        if constants.SOURCES.validate(source) and not source in self.sources:
            bisect.insort(self._sources, source)

    def remove_source(self, source):
        try:
            self._sources.remove(source)
        except ValueError:
            pass

    @property
    def csv_out_dialect(self):
        return self._csv_out_dialect

    @csv_out_dialect.setter
    def csv_out_dialect(self, value):
        if constants.CSV_OUT_DIALECTS.validate(value):
            self._csv_out_dialect = value

    def from_file(self, path):
        # Try to open the given path and read the json data in it.
        # Catch the FileNotFound from `open` and raise custom exception if needed
        # also handle the file read error
        try:
            with open(path) as file:
                data = json.loads(file.read())
        except FileNotFoundError as e:
            my_exception = exceptions.MissingFile(path)
            self._add_err(str(my_exception))
            self.settings_loaded = False
            raise my_exception
        except: # catch everything else, especially json read errors
            my_exception = exceptions.FileReadError(path)
            self._add_err(str(my_exception))
            self.settings_loaded = False
            raise my_exception


        def is_set(field_name):
            return (field_name in data
                and data[field_name] is not None
                and len(data[field_name]) > 0
                )

        if is_set(constants.FIELDS.START):
            self.start_date = data[constants.FIELDS.START]
        if is_set(constants.FIELDS.END):
            self.end_date = data[constants.FIELDS.END]
        if is_set(constants.FIELDS.TYPE):
            try:
                self.output_type = data[constants.FIELDS.TYPE]
            except exceptions.OutputTypeException as e:
                self._add_err(str(e))
                self.output_type = constants.OUTPUT_TYPE.SINGLE_TICKER
        if is_set(constants.FIELDS.PATH):
            self.output_path = data[constants.FIELDS.PATH] or self.default_output_path
        if is_set(constants.FIELDS.TICKERS):
            self._tickers = data[constants.FIELDS.TICKERS]
        if is_set(constants.FIELDS.SOURCES):
            for source in data[constants.FIELDS.SOURCES]:
                try:
                    self.add_source(source)
                except exceptions.SourceException as e:
                    self._add_err(str(e))
        if is_set(constants.FIELDS.CSV_DIALECT):
            try:
                self.csv_out_dialect = data[constants.FIELDS.CSV_DIALECT]
            except:
                pass
        if is_set(constants.FIELDS.SETTINGS_PATH):
            self.settings_path = data[constants.FIELDS.SETTINGS_PATH]
        
        self.settings_loaded = True
        return self.settings_loaded

    def serialize(self):
        data = {}
        if self.start_date is not None:
            data[constants.FIELDS.START] = self.start_date.strftime("%Y-%m-%d")
        else:
            data[constants.FIELDS.START] = None
        if self.end_date is not None:
            data[constants.FIELDS.END] = self.end_date.strftime("%Y-%m-%d")
        else:
            data[constants.FIELDS.END] = None

        data[constants.FIELDS.TYPE] = self.output_type
        data[constants.FIELDS.PATH] = self.output_path or self.default_output_path
        data[constants.FIELDS.TICKERS] = self.tickers
        data[constants.FIELDS.SOURCES] = self._sources
        data[constants.FIELDS.CSV_DIALECT] = self.csv_out_dialect
        data[constants.FIELDS.SETTINGS_PATH] = self.settings_path or self.__default_settings_path

        return data

    def to_file(self, path=None):
        if not path:
            path = self.settings_path

        if not os.path.exists(path):
            # TODO: Create path
            pass
        
        try:
            full_path = os.path.abspath(path)
            with open(full_path, "w") as file:
                file.write(json.dumps(self.serialize(), indent=2))

        except Exception as e:
            self._add_err(str(e))
            return False
        return True

    def _add_err(self, err):
        self.errors.append(err)
