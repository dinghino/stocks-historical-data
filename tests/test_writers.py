import csv
from tests import utils

from stonks.components import writers
from stonks.constants import SOURCES

# Fake CSV lines for the parser to produce its cache and pass it to the writer
# The parser itself is tested in its own module so we assume it's working and
# can be used here to test the writer's behaviour with that data
TEST_HEADER = [
    "Date",
    "Symbol",
    "ShortVolume",
    "ShortExemptVolume",
    "TotalVolume",
    "Market"]
TEST_DATA_MULTI = [
    ["20210427", "A", "109763", "1", "244138", "B,Q,N"],
    ["20210427", "MTG", "158897", "0", "744287", "Q,N"],
    ["20210427", "SRL", "13359", "830", "23154", "Q,N"]
]
TEST_DATA_SINGLE = [
    ["20210427", "GME", "2291953", "44637", "3972777", "B"],
    ["20210428", "GME", "1420847", "32918", "2528395", "B"],
]


def get_default_filepath_single():
    return utils.get_file_path("20210427-20210427_FINRA_SV_GME.csv")


def get_default_filepaths_multi():
    return (
        utils.get_file_path("20210427-20210427_FINRA_SV_A.csv"),
        utils.get_file_path("20210427-20210427_FINRA_SV_MTG.csv"),
        utils.get_file_path("20210427-20210427_FINRA_SV_SRL.csv"),
    )


def get_custom_filepath_single():
    return utils.get_file_path("custom.csv")


def validate_written_file(paths, header, data):
    # Get all the rows from the parser data stored in [ticker]: [row_data,]
    compare = [row for t in sorted(list(data.keys())) for row in data[t]]
    output = []
    for path in paths:
        with open(path, 'r') as file:
            assert file is not None
            reader = csv.reader(file.read().splitlines())
            # compare the file header with the parsed header
            assert next(reader) == header
            for row in reader:
                # for each file path provided take all the rows and add them to
                # the output list
                output.append(row)
    # After all files are done compare one-one the content of the lists
    for i, row in enumerate(output):
        assert row == compare[i]


class TestSingleWriter:

    @utils.decorators.setup_component(writers.SingleFile)
    def test_write_no_data(self, writer, *args, **kwargs):
        header = []
        data = {}
        assert writer.write(header, data, SOURCES.FINRA_SHORTS) is False

    @utils.decorators.delete_file(get_default_filepath_single())
    @utils.decorators.setup_component(writers.SingleFile)
    @utils.decorators.writer_data(TEST_HEADER, TEST_DATA_SINGLE)
    def test_write(self, writer, header, data, *args, **kwargs):

        full_path = get_default_filepath_single()
        writer.write(header, data, SOURCES.FINRA_SHORTS)

        validate_written_file([full_path], header, data)

    @utils.decorators.delete_file(get_custom_filepath_single())
    @utils.decorators.setup_component(writers.SingleFile)
    @utils.decorators.writer_data(TEST_HEADER, TEST_DATA_SINGLE)
    def test_write_custom_name(self, writer, header, data, *args, **kwargs):

        full_path = get_custom_filepath_single()
        writer.settings.output_path = full_path
        writer.write(header, data, SOURCES.FINRA_SHORTS)

        validate_written_file([full_path], header, data)


class TestMultiWriter:

    @utils.decorators.setup_component(writers.MultiFile)
    def test_write_no_data(self, writer, *args, **kwargs):
        header = []
        data = {}
        assert writer.write(header, data, SOURCES.FINRA_SHORTS) is False

    @utils.decorators.delete_file(*get_default_filepaths_multi())
    @utils.decorators.setup_component(writers.MultiFile)
    @utils.decorators.writer_data(TEST_HEADER, TEST_DATA_MULTI)
    def test_write(self, writer, header, data, *args, **kwargs):

        writer.write(header, data, SOURCES.FINRA_SHORTS)

        # FIXME: This is not working for multifile. either change the validate
        # function or set up something different
        validate_written_file(get_default_filepaths_multi(), header, data)

    # @utils.decorators.delete_file(get_custom_filepath_single())
    # @utils.decorators.setup_component(writers.MultiFile)
    # @utils.decorators.writer_data(TEST_HEADER, TEST_DATA_MULTI)
    # def test_write_custom_name(self, writer, header, data, *args, **kwargs):

    #     full_path = get_custom_filepath_single()
    #     writer.settings.output_path = full_path
    #     writer.write(header, data, SOURCES.FINRA_SHORTS)

    #     with open(full_path) as file:
    #         assert file is not None
    #         validate_written_file(full_path, header, data)
