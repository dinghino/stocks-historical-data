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
    def write(self, data, source):
        raise NotImplementedError

    def write_to_file(self, path, filename, data):
        # ensure path exists and create it if missing
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(path + filename, "w", newline="") as csvfile:
            # TODO: Implement dialects at least:
            # - default with '|' delimiter,
            # - excel, csv default one
            # Add to cli, settings etc.
            wr = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
            for line in data:
                wr.writerow(line) 
