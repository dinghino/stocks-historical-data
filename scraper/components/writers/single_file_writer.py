from scraper.components.writers.base_writer import Writer


class SingleFileWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def _create_filename(self, tickers):
        # if we asked for too many tickers the "usual" filename would be too long
        # for most systems (~9000 tickers?) so we just use the date
        base_filename = "{}_{}".format(
            self.settings.start_date,
            self.settings.end_date
        )
        
        if len(tickers) > 5:
            return "{}_FINRA.csv".format(base_filename)

        sanitized = []
        for ticker in tickers:
            sanitized.append(self.sanitize_ticker(ticker))

        return "{}_{}.csv".format(base_filename,"_".join(sanitized))

    def write(self, source):
        if len(source) is 0:
            raise Exception("Writer received an empty source. cannot write")

        filename = self.get_filename_from_settings(source.keys())
        path = self.get_path_from_settings()
        # get the header from the first dataset
        header = source[list(source.keys())[0]][0]
        data = [header,]

        for ticker, data in source.items():
            # first row is the header. we already have that, so skip for each set
            for row in data[1:]:
                data.append(row)

        self._write_to_file(path, filename, data)
