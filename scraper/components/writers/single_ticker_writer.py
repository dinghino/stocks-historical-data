from scraper.components.writers.base_writer import Writer


class SingleTickerWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def _create_filename(self, ticker):
        return "{}_{}_{}.csv".format(
            self.settings.start_date,
            self.settings.end_date,
            self.sanitize_ticker(ticker),
            )

    def write(self, source):
        path = self.get_path_from_settings()
        for ticker, data in source.items():
            filename = self.get_filename_from_settings(ticker)
            self._write_to_file(path, filename, data)
