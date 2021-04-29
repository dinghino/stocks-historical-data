from scraper.components.writers.base_writer import Writer


class SingleTickerWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def write(self, header, data, source):
        path = self.fname_gen.get_path()
        success = True
        for ticker, data in data.items():
            filename = self.fname_gen.get_filename(ticker, source)
            to_write = [header,]
            for row in data:
                to_write.append(row)
            success = success and self.write_to_file(path, filename, to_write)
        return success

