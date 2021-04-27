from scraper.components.writers.base_writer import Writer


class SingleTickerWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def write(self, data, source):
        path = self.fname_gen.get_path()
        success = True
        for ticker, data in data.items():
            filename = self.fname_gen.get_filename(ticker, source)
            success = success and self.write_to_file(path, filename, data)
        return success

