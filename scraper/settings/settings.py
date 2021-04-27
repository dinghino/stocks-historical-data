import os
import time
import json
import bisect
import datetime

import click

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
        self._out_type = Settings.OUTPUT_TYPE.SINGLE_FILE
        self._out_path = self.default_output_path
        self._csv_out_dialect = ''

        self.debug = False
        self.path_with_filename = False
        
        if (settings_path):
            self.settings_path = settings_path

    def init(self, path=None):
        if not path:
            path = self.settings_path

        try:
            self.from_file(path)
            return True
        except exceptions.MissingFile:
            print("Could not load from defined path, trying default.")
            try:
                self.from_file(self.settings_path)
                return True
            except exceptions.MissingFile:
                print("Could not load from default path, starting empty.")
                return True


    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def tickers(self):
        return self._tickers

    @property
    def output_type(self):
        return self._out_type

    @property
    def output_path(self):
        return self._out_path

    @property
    def sources(self):
        return self._sources

    @property
    def csv_out_dialect(self):
        return self._csv_out_dialect

    @start_date.setter
    def start_date(self, date):
        self._start_date = self._parse_datestr(date, 'start date')

    @end_date.setter
    def end_date(self, date):
        self._end_date = self._parse_datestr(date, 'end date')

    @output_type.setter
    def output_type(self, value):
        if not Settings.OUTPUT_TYPE.validate(value):
            raise exceptions.OutputTypeException(value)
        self._out_type = value

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

    def _parse_datestr(self, datestr, excpt_msg):
        for frmt in Settings.VALID_DATES_FORMAT:
            try:
                return datetime.datetime.strptime(datestr, frmt).date()
            except ValueError:
                pass

        valid = ", ".join(Settings.VALID_DATES_FORMAT)
        raise exceptions.DateException(datestr, excpt_msg)

    def add_source(self, source):
        if not Settings.SOURCES.validate(source):
            raise exceptions.SourceException(source)
        bisect.insort(self._sources, source)

    def remove_source(self, source):
        try:
            self._sources.remove(source)
        except ValueError:
            pass

    def from_file(self, path=None):
        if not path:
            path = self.settings_path
        try:
            print("Reading settings from {}".format(path))
            with open(path) as file:
                data = json.loads(file.read())
        except:
            raise exceptions.MissingFile(path)

        def is_set(field_name):
            return (field_name in data
                and data[field_name] is not None
                and len(data[field_name]) > 0
                )


        if is_set(Settings.FIELDS.START):
            self.start_date = data['Start']
        if is_set(Settings.FIELDS.END):
            self.end_date = data[Settings.FIELDS.END]
        if is_set(Settings.FIELDS.TYPE):
            try:
                self.output_type = data[Settings.FIELDS.TYPE]
            except exceptions.OutputTypeException as e:
                print(e)
                print("Resetting output type value to default.")
                self.output_type = Settings.OUTPUT_TYPE.SINGLE_TICKER
                time.sleep(1)
        if is_set(Settings.FIELDS.PATH):
            self.output_path = data[Settings.FIELDS.PATH] or self.default_output_path
        if is_set(Settings.FIELDS.TICKERS):
            self._tickers = data[Settings.FIELDS.TICKERS]
        if is_set(Settings.FIELDS.SOURCES):
            for source in data[Settings.FIELDS.SOURCES]:
                try:
                    self.add_source(source)
                except exceptions.SourceException as e:
                    click.echo(e)
                    click.echo("Could not add source {}. Skipping".format(source))

        if is_set(Settings.FIELDS.SETTINGS_PATH):
            self.settings_path = data[Settings.FIELDS.SETTINGS_PATH]

    def serialize(self):
        data = {}
        if self.start_date is not None:
            data[Settings.FIELDS.START] = self.start_date.strftime("%Y-%m-%d")
        else:
            data[Settings.FIELDS.START] = None
        if self.end_date is not None:
            data[Settings.FIELDS.END] = self.end_date.strftime("%Y-%m-%d")
        else:
            data[Settings.FIELDS.END] = None

        data[Settings.FIELDS.TYPE] = self.output_type
        data[Settings.FIELDS.PATH] = self.output_path or self.default_output_path
        data[Settings.FIELDS.TICKERS] = self.tickers
        data[Settings.FIELDS.SOURCES] = self._sources
        data[Settings.FIELDS.SETTINGS_PATH] = self.settings_path or self.__default_settings_path

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
            print(e)
            return False
        return True