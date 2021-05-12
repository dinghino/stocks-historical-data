from stonks.components.base_writer import WriterBase
from .constants import output_type


class SingleTickerWriter(WriterBase):
    """Writer class to generate one file for each ticker/symbol in the dataset.
    The incoming data (from the parsers) can be missing the ticker/symbol as
    that is the only one present in the file itself.
    """
    @staticmethod
    def is_for():
        return output_type

    def set_parse_rows(self):
        return True

    def generate_file_data(self, header, data, source):
        if not data:
            return False

        path = self.fname_gen.get_path()

        # success = True

        for ticker, data in sorted(data.items()):
            filename = self.fname_gen.get_filename(ticker, source)
            to_write = [header]
            for row in data:
                to_write.append(row)
            yield (path, filename, to_write, [ticker])
