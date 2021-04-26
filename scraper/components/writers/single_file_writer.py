from scraper.components.writers.base_writer import Writer


class SingleFileWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def write(self, data, source):
        if len(data) is 0:
            raise Exception("Writer received an empty data. cannot write")

        filename = self.fname_gen.get_filename(data.keys(), source)
        path = self.fname_gen.get_path()
        # get the header from the first dataset
        header = data[list(data.keys())[0]][0]
        output = [header,]

        for _, rows in data.items():
            # first row is the header. we already have that, so skip for each set
            for row in rows[1:]:
                output.append(row)

        self.write_to_file(path, filename, output)
