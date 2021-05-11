import abc
import csv
import os
from pathlib import Path

from stonks.components.base_component import ComponentBase

from .filename import FilenameGenerator


class WriterBase(ComponentBase):
    class Result:
        def __init__(self, success, path):
            self.success = success
            self.path = path

    def __init__(self, settings, debug=False):
        self.settings = settings
        self.base_path = settings.output_path
        self.fname_gen = FilenameGenerator(settings)
        self.settings.parse_rows_from_writer = self.set_parse_rows()

    @abc.abstractmethod
    def set_parse_rows(self):   # pragma: no cover
        return NotImplemented

    @abc.abstractmethod
    def generate_file_data(self, header, data, source):  # pragma: no cover
        return NotImplemented

    def write_to_file(self, path, filename, data):
        # ensure path exists and create it if missing
        full_path = self.get_full_path(path, filename)

        with open(full_path, "w", newline="") as csvfile:
            wr = csv.writer(csvfile, dialect=self.settings.csv_out_dialect)
            for line in data:
                wr.writerow(line)

        return WriterBase.Result(True, full_path)

    def write(self, header, data, source):
        if not data:
            yield WriterBase.Result(False, None)

        data_generator = self.generate_file_data(header, data, source)
        for (path, fname, data) in data_generator:
            yield self.write_to_file(path, fname, data)

    def get_full_path(self, path, filename):
        """Returns the full path for the file.
        Also ensures that the dir path exists, creating folders as needed
        if `mkpath` is True"""
        Path(path).mkdir(parents=True, exist_ok=True)
        return os.path.join(path, filename)
