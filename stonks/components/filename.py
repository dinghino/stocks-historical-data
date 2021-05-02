import os
from stonks import utils


class FilenameGenerator:
    default_fname_template = "{start}-{end}_{source}_{tickers}"
    extension = ".csv"
    default_path = "./data/output/"

    def __init__(self, settings, tickers_max_count=5):
        self.settings = settings
        self.tickers_max_count = tickers_max_count

    def get_filename(self, tickers, source):
        # If the user specified a filename in the output path we use that
        # TODO: Remember to check if the file exists and ask for override
        # in the CLI
        if utils.path_contains_filename(self.settings.output_path):
            _, fname = os.path.split(self.settings.output_path)
            return fname

        # TODO: Assemble the filename
        filename = self.select_fname_template().format(
            start=self.settings.start_date.strftime('%Y%m%d'),
            end=self.settings.end_date.strftime('%Y%m%d'),
            source=self.get_source_appendix(source),
            tickers=self.format_tickers(tickers)
        )
        if len(tickers) > self.tickers_max_count:   # pragma: no cover
            filename += "_MORE"

        return filename + self.extension

    def format_tickers(self, tickers):
        out = []
        # try:
        if type(tickers) is str:
            aval = [tickers]        # single ticker passed
        else:
            aval = list(tickers)    # list or dict_keys (not indexable)

        aval = sorted(aval)

        for i in range(0, min(len(aval), self.tickers_max_count)):
            out.append(self.sanitize_ticker(aval[i]))

        return '_'.join(out)

    def get_path(self):
        path = self.settings.output_path
        if not path:  # pragma: no cover
            return self.default_path

        if utils.path_contains_filename(path):
            path, _ = os.path.split(self.settings.output_path)

        if not path.endswith('/'):
            path += "/"

        return path

    def get_source_appendix(self, source):  # pragma: no cover
        if source == self.settings.SOURCES.FINRA_SHORTS:
            return "FINRA_SV"
        if source == self.settings.SOURCES.SEC_FTD:
            return "SEC_FTD"
        return ""

    def sanitize_ticker(self, ticker):
        return ticker.replace("/", "")

    def select_fname_template(self):
        # TODO: Placeholder function for when we'll allow custom formatting
        # from CLI
        return self.default_fname_template
