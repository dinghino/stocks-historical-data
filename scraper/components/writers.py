import csv
from datetime import datetime
from pathlib import Path

class SingleTickerWriter:
    def __init__(self, base_path="./"):
        self.base_path = base_path
        self. today = datetime.now().date().strftime("%Y%m%d")

    def _write_to_file(self, filename, data):
        # Create the path if it does not exist
        Path(self.base_path).mkdir(parents=True, exist_ok=True)

        with open(self.base_path + filename, "w", newline="") as csvfile:
            wr = csv.writer(csvfile, delimiter='|', quotechar="|", quoting=csv.QUOTE_MINIMAL)
            for line in data:
                wr.writerow(line) 

    def _create_filename(self, ticker):
        return "{}_{}.csv".format(self.today,self.sanitize_ticker(ticker))

    def write(self, source):
        for ticker, data in source.items():
            filename = self._create_filename(ticker)
            self._write_to_file(filename, data)

    def sanitize_ticker(self, ticker):
        # TODO: Take the ticker string and clean up os-restricted characters like / ? and so on
        return ticker.replace("/","-")


class SingleFileWriter(SingleTickerWriter):
    def __init__(self, base_path="./"):
        super().__init__(base_path)

    def _create_filename(self, tickers):
        # if we asked for too many tickers the "usual" filename would be too long
        # for most systems (~9000 tickers?) so we just use the date
        if len(tickers) > 5:
            return "{}_FINRA.csv".format(self.today)

        sanitized = []
        for ticker in tickers:
            sanitized.append(self.sanitize_ticker(ticker))

        return "{}_{}.csv".format(self.today,"_".join(sanitized))

    def write(self, source):
        if len(source) is 0:
            raise Exception("Writer received an empty source. cannot write")

        # generate the filename with all the tickers
        filename = self._create_filename(source.keys())
        # get the header from the first dataset
        header = source[list(source.keys())[0]][0]
        output = [header,]

        for ticker, data in source.items():
            # first row is the header. we already have that, so skip for each set
            for row in data[1:]:
                output.append(row)

        self._write_to_file(filename, output)
