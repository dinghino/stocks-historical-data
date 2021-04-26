from scraper.components.writers.base_writer import Writer


class SingleTickerWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def write(self, data, source):
        path = self.fname_gen.get_path()
        for ticker, data in data.items():
            filename = self.fname_gen.get_filename(ticker, source)
            self.write_to_file(path, filename, data)

