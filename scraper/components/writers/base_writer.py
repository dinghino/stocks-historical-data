import abc
import csv
from datetime import datetime
from pathlib import Path

from scraper import utils
from scraper.components.writers.filename import FilenameGenerator

class Writer(abc.ABC):
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.base_path = settings.output_path
        self.fname_gen = FilenameGenerator(settings)

        self.today = datetime.now().date().strftime("%Y%m%d")

    @abc.abstractmethod
    def write(self, header, data, source):
        raise NotImplementedError

    def write_to_file(self, path, filename, data):
        # ensure path exists and create it if missing
        Path(path).mkdir(parents=True, exist_ok=True)
        # add our custom dialects (available should be 'excel' and 'default')
        utils.register_custom_csv_dialects()

        with open(path + filename, "w", newline="") as csvfile:
            wr = csv.writer(csvfile, dialect=self.settings.csv_out_dialect)
            for line in data:
                wr.writerow(line)

        return True
