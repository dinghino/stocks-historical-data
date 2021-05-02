from stonks.scraper.settings.constants import OUTPUT_TYPE
from stonks.scraper.components.writers.base_writer import Writer


class SingleTickerWriter(Writer):
    """Writer class to generate one file for each ticker/symbol in the dataset.
    The incoming data (from the parsers) can be missing the ticker/symbol as
    that is the only one present in the file itself.
    """
    @staticmethod
    def is_for():
        return OUTPUT_TYPE.SINGLE_TICKER

    def write(self, header, data, source):
        if not data:
            return False
        path = self.fname_gen.get_path()
        success = True
        for ticker, data in data.items():
            filename = self.fname_gen.get_filename(ticker, source)
            to_write = [header]
            for row in data:
                to_write.append(row)
            success = success and self.write_to_file(path, filename, to_write)
        return success
