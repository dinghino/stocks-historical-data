import os
import time
import json
import bisect
import datetime

import click

valid_date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%y-%m-%d", "%y/%m/%d", ]

class Settings:

    class FIELDS:
        START = "Start"
        END = "End"
        TYPE ="Type"
        PATH ="Path"
        TICKERS ="Tickers"
        SOURCES = "Sources"
        SETTINGS_PATH ="settings_path"

    class OUTPUT_TYPE:
        SINGLE_FILE = "Aggregate File"
        SINGLE_TICKER = "Individual Ticker files"
        VALID = [SINGLE_FILE, SINGLE_TICKER]
        @staticmethod
        def validate(value):
            return value in Settings.OUTPUT_TYPE.VALID

    class SOURCES:
        FINRA_SHORTS = "FINRA Short reports"
        SEC_FTD = "SEC FTDs"
        VALID = [FINRA_SHORTS, SEC_FTD]
        @staticmethod
        def validate(value):
            return value in Settings.SOURCES.VALID

    class DateException(ValueError):
        def __init__(self, datestr, field, *args):

            valid = ", ".join(valid_date_formats)
            self.message = "Could not parse {0} for '{1}'. Valid formats are: {2}".format(
                datestr, field, valid)
            # if args: self.message = args[0]
            # else: self.message = "There was an error while setting a date"
        def __str__(self):
            return "Settings.DateException: {0}".format(self.message)

    class OutputTypeException(ValueError):
        def __init__(self, val, *args):
            self.message = "Provided value '{}' is not valid. should be one of '{}'".format(
                val, ", ".join(Settings.OUTPUT_TYPE.VALID))
        def __str__(self):
            return self.message

    class SourceException(ValueError):
        def __init__(self, val, *args):
            self.message = "Provided value '{}' is not valid. should be one of '{}'".format(
                val, ", ".join(Settings.SOURCES.VALID))
        def __str__(self):
            return self.message

    class MissingFile(Exception):
        def __str__(self):
            return 'Settings file not found at {}'.format(Settings.settings_path)

    settings_path = './data/options.json'

    def __init__(self, settings_path=None):
        self._start_date = None
        self._end_date = None
        self._tickers = []
        self._sources = []
        self._out_type = Settings.OUTPUT_TYPE.SINGLE_FILE
        self._out_path = "./"
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
        except Settings.MissingFile:
            print("Could not load from defined path, trying default.")
            try:
                self.from_file(self.settings_path)
                return True
            except Settings.MissingFile:
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

    @start_date.setter
    def start_date(self, date):
        self._start_date = self._parse_datestr(date, 'start date')

    @end_date.setter
    def end_date(self, date):
        self._end_date = self._parse_datestr(date, 'end date')

    @output_type.setter
    def output_type(self, value):
        if not Settings.OUTPUT_TYPE.validate(value):
            raise Settings.OutputTypeException(value)
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
        for frmt in valid_date_formats:
            try:
                return datetime.datetime.strptime(datestr, frmt).date()
            except ValueError:
                pass

        valid = ", ".join(valid_date_formats)
        raise Settings.DateException(datestr, excpt_msg)

    def add_source(self, source):
        if not Settings.SOURCES.validate(source):
            raise Settings.SourceException(source)
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
            raise Settings.MissingFile

        def is_set(field_name):
            return field_name in data and len(data[field_name]) > 0


        if is_set(Settings.FIELDS.START):
            self.start_date = data['Start']
        if is_set(Settings.FIELDS.END):
            self.end_date = data[Settings.FIELDS.END]
        if is_set(Settings.FIELDS.TYPE):
            try:
                self.output_type = data[Settings.FIELDS.TYPE]
            except Settings.OutputTypeException as e:
                print(e)
                print("Resetting output type value to default.")
                self.output_type = Settings.OUTPUT_TYPE.SINGLE_TICKER
                time.sleep(1)
        if is_set(Settings.FIELDS.PATH):
            self.output_path = data[Settings.FIELDS.PATH]
        if is_set(Settings.FIELDS.TICKERS):
            self._tickers = data[Settings.FIELDS.TICKERS]
        if is_set(Settings.FIELDS.SOURCES):
            for source in data[Settings.FIELDS.SOURCES]:
                try:
                    self.add_source(source)
                except Settings.SourceException as e:
                    click.echo(e)
                    click.echo("Could not add source {}. Skipping".format(source))

        if Settings.FIELDS.SETTINGS_PATH in data and is_set(data[Settings.FIELDS.SETTINGS_PATH]):
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
        data[Settings.FIELDS.PATH] = self.output_path
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
