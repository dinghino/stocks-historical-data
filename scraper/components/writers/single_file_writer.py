from scraper.settings.constants import OUTPUT_TYPE
from scraper.components.writers.base_writer import Writer


class SingleFileWriter(Writer):
    """Writer class to aggregate more ticker/symbols contained in the incoming
    data into a single file. Data rows SHOULD then contain a reference to an
    unique identifier to that symbol, otherwise the data would be unusable.
    """
    @staticmethod
    def is_for():
        return OUTPUT_TYPE.SINGLE_FILE

    def write(self, header, data, source):
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

        # generate a sorted-by-ticker list of data
        # TODO: Add option to define sorting methods
        for ticker in sorted(list(tickers)):
            for row in data[ticker]:
                output.append(row)
        # old method, unsorted mess of data. kept for reference
        # for _, rows in data.items():
        #     for row in rows:
        #         output.append(row)

        return self.write_to_file(path, filename, output)
