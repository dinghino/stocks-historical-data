import datetime
import bisect
import json
import os

valid_date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%y-%m-%d", "%y/%m/%d", ]


class Settings:

    class OUTPUT_TYPE:
        SINGLE_FILE = "SINGLE_FILE"
        SINGLE_TICKER = "SINGLE_TICKER"
        VALID = [SINGLE_FILE, SINGLE_TICKER]

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
            self.message = "Provided value '{}' is not valid. should be one of '{}'".format(val, ", ".join(Settings.OUTPUT_TYPE.VALID))
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

    @start_date.setter
    def start_date(self, date):
        self._start_date = self._parse_datestr(date, 'start date')

    @end_date.setter
    def end_date(self, date):
        self._end_date = self._parse_datestr(date, 'end date')

    @output_type.setter
    def output_type(self, value):
        if value not in Settings.OUTPUT_TYPE.VALID:
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

    def from_file(self, path=None):
        if not path:
            path = self.settings_path
        try:
            print("Reading settings from {}".format(path))
            with open(path) as file:
                data = json.loads(file.read())
        except:
            raise Settings.MissingFile

        if 'Start' in data and len(data['Start']) > 0:
            self.start_date = data['Start']
        if 'End' in data and len(data['End']) > 0:
            self.end_date = data['End']
        if 'Type' in data and len(data['Type']) > 0:
            self.output_type = data['Type']
        if 'Path' in data and len(data['Path']) > 0:
            self.output_path = data['Path']
        if 'Tickers' in data and len(data['Tickers']) > 0:
            self._tickers = data['Tickers']
            # TODO: Loop instead of replacing?
            # for ticker in data['Tickers']:
            #     self.add_ticker(ticker)
        if 'settings_path' in data and len(data['settings_path']) > 0:
            self.settings_path = data['settings_path']

    def serialize(self):
        data = {}
        if self.start_date is not None:
            data["Start"] = self.start_date.strftime("%Y-%m-%d")
        else:
            data["Start"] = None
        if self.end_date is not None:
            data["End"] = self.end_date.strftime("%Y-%m-%d")
        else:
            data["End"] = None
        data["Type"] = self.output_type
        data["Path"] = self.output_path
        data["Tickers"] = self.tickers
        data["settings_path"] = self.settings_path or self.__default_settings_path
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


if __name__ == "__main__":
    OPTIONS_PATH = "../data/options.json"

    test_tickers = "amc gme bb tsla brk/a TSLA ge msft pltr boa jpm".split()
    start_date = "2020/5/1"
    end_date = "2021-4-25"
    out_type = Settings.OUTPUT_TYPE.SINGLE_FILE
    out_path = './folder'
    def test1():
        settings = Settings()
        print("\n>> Testing date management")
        settings.start_date = start_date
        settings.end_date = end_date
        print(settings.start_date)
        print(settings.end_date)

        print("\n>> Testing ticker management")

        print(test_tickers)
        for tick in test_tickers:
            settings.add_ticker(tick)
        print(settings.tickers)

        print("\n>> Testing WRONG output type")
        try:
            settings.output_type = "WRONG"
        except Settings.OutputTypeException as e:
            print(e)
        print(settings.output_type)
        print("\n>> Testing valid Output Type")
        settings.output_type = out_type
        print(settings.output_type)

        print("\n>> Testing Output Path")
        print('out contains filename: {}'.format(settings.path_with_filename))
        settings.output_path = './data.csv'
        print(settings.output_path)
        print('out contains filename: {}'.format(settings.path_with_filename))
        settings.output_path = out_path
        print(settings.output_path)
        print('out contains filename: {}'.format(settings.path_with_filename))

    def test2():
        settings = Settings()
        if settings.init(path=OPTIONS_PATH):
            print(">> Settings initialized. Begin Testing")

        print(settings.serialize())

        
        settings.start_date = start_date
        settings.end_date = end_date
        settings.output_type = out_type
        settings.output_path = out_path
        for tick in test_tickers:
            settings.add_ticker(tick)
        print(settings.serialize())
        print(">> Attempting to save settings")
        settings.to_file(path=OPTIONS_PATH)

    # test1()
    # test2()
