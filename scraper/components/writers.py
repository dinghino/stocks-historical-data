import abc
import csv
from datetime import datetime
from pathlib import Path

def path_contains_filename(path):
    if path[-4:] in ['.csv', '.txt']:
        return True
    return False

class Writer(abc.ABC):
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.base_path = settings.output_path

        self.today = datetime.now().date().strftime("%Y%m%d")

    def get_path_from_settings(self):
        path = self.settings.output_path
        if path_contains_filename(path):
            split = self.settings.output_path.split('/')
            path = '/'.join(split[:-1])
        
        if path[-1] is not '/':
            path += "/"

        return path

    def get_filename_from_settings(self, content):
        if not path_contains_filename(self.settings.output_path):
            return self._create_filename(content)

        return self.settings.output_path.split('/')[-1]

    def sanitize_ticker(self, ticker):
        # TODO: Take the ticker string and clean up os-restricted characters like / ? and so on
        return ticker.replace("/","-")

    @abc.abstractmethod
    def _create_filename(self):
        raise NotImplementedError

    @abc.abstractmethod
    def write(self):
        raise NotImplementedError

    def _write_to_file(self, path, filename, data):
        # ensure path exists and create it if missing
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(path + filename, "w", newline="") as csvfile:
            wr = csv.writer(csvfile, delimiter='|', quotechar="|", quoting=csv.QUOTE_MINIMAL)
            for line in data:
                wr.writerow(line) 


class SingleTickerWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def _create_filename(self, ticker):
        return "{}_{}_{}.csv".format(
            self.settings.start_date, self.settings.end_date ,self.sanitize_ticker(ticker)
            )

    def write(self, source):
        path = self.get_path_from_settings()
        for ticker, data in source.items():
            filename = self.get_filename_from_settings(ticker)
            self._write_to_file(path, filename, data)


class SingleFileWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def _create_filename(self, tickers):
        # if we asked for too many tickers the "usual" filename would be too long
        # for most systems (~9000 tickers?) so we just use the date
        base_filename = "{}_{}".format(self.settings.start_date, self.settings.end_date)
        
        if len(tickers) > 5:
            return "{}_FINRA.csv".format(base_filename)

        sanitized = []
        for ticker in tickers:
            sanitized.append(self.sanitize_ticker(ticker))

        return "{}_{}.csv".format(base_filename,"_".join(sanitized))

    def write(self, source):
        if len(source) is 0:
            raise Exception("Writer received an empty source. cannot write")

        filename = self.get_filename_from_settings(source.keys())
        path = self.get_path_from_settings()
        # get the header from the first dataset
        header = source[list(source.keys())[0]][0]
        data = [header,]

        for ticker, data in source.items():
            # first row is the header. we already have that, so skip for each set
            for row in data[1:]:
                data.append(row)

        self._write_to_file(path, filename, data)
