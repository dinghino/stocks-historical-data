from scraper.components.writers.base_writer import Writer


class SingleFileWriter(Writer):
    def __init__(self, settings, debug=False):
        super().__init__(settings, debug)

    def write(self, header, data, source):
        # NOTE: This can happen when the fetcher could not find the data, the
        # parser had issues parsing existing data or mixed conditions.
        # One example would be for the SEC FTD data of the current month that
        # does not actually exist, apparently.
        if len(data) is 0:
            return False

        filename = self.fname_gen.get_filename(data.keys(), source)
        path = self.fname_gen.get_path()
        output = [header,]

        for _, rows in data.items():
            # first row is the header. we already have that, so skip for each set
            # for row in rows[1:]:
            for row in rows:
                output.append(row)

        return self.write_to_file(path, filename, output)
