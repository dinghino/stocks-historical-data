from stonks.components.base_writer import WriterBase
from .constants import output_type


class SingleFileWriter(WriterBase):
    """Writer class to aggregate more ticker/symbols contained in the incoming
    data into a single file. Data rows SHOULD then contain a reference to an
    unique identifier to that symbol, otherwise the data would be unusable.
    """
    @staticmethod
    def is_for():
        return output_type

    def set_parse_rows(self):
        return False

    def generate_file_data(self, header, data, source):
        # NOTE: This can happen when the fetcher could not find the data, the
        # parser had issues parsing existing data or mixed conditions.
        # One example would be for the SEC FTD data of the current month that
        # does not actually exist, apparently.

        if not data:
            return False

        tickers = data.keys()

        filename = self.fname_gen.get_filename(tickers, source)
        path = self.fname_gen.get_path()
        output = [header]
        for _, rows in sorted(data.items()):
            for row in rows:
                output.append(row)
        yield (path, filename, output, sorted(tickers))
