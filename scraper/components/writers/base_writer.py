import abc
import csv
from datetime import datetime
from pathlib import Path

from scraper import utils

class Writer(abc.ABC):
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.base_path = settings.output_path

        self.today = datetime.now().date().strftime("%Y%m%d")

    def get_path_from_settings(self):
        path = self.settings.output_path
        if utils.path_contains_filename(path):
            split = self.settings.output_path.split('/')
            path = '/'.join(split[:-1])
        
        if path[-1] is not '/':
            path += "/"

        return path

    def get_filename_from_settings(self, content):
        if not utils.path_contains_filename(self.settings.output_path):
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
