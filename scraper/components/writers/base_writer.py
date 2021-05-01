import abc
import csv
from pathlib import Path

from scraper import utils
from scraper.components.component_base import ComponentBase
from scraper.components.writers.filename import FilenameGenerator


class Writer(ComponentBase):
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.base_path = settings.output_path
        self.fname_gen = FilenameGenerator(settings)

    @abc.abstractmethod
    def write(self, header, data, source):  # pragma: no cover
        return NotImplemented

    def write_to_file(self, path, filename, data):
        # ensure path exists and create it if missing
        Path(path).mkdir(parents=True, exist_ok=True)
        # add our custom dialects (available should be 'excel' and 'default')
        utils.register_custom_csv_dialects(manager.get_dialects())

        with open(path + filename, "w", newline="") as csvfile:
            wr = csv.writer(csvfile, dialect=self.settings.csv_out_dialect)
            for line in data:
                wr.writerow(line)

        return True

# FIXME: Refactor things around to avoid this ugly import.
# Manager classes at some point require component base classes so
# this causes circular imports and break stuff. For now putting it at the end
# works, but indicates flaws in the structure.
# IDEA: refactor _everything_ to provide manager to all components when
# instantiating them?
from scraper.components import manager  # noqa
