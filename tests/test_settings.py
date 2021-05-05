import os
import json
import datetime

import pytest

from tests import mocks, utils
from stonks import exceptions, Settings, manager
from stonks.components.writers import aggregate_writer, ticker_writer
from stonks.components.handlers import finra

Settings.settings_path = mocks.constants.SETTINGS_PATH


# MAYBE TODO: Properly validate all the data?
def validate_start_date(settings):
    assert settings.start_date == utils.get_expected_start_date()


class TestSettings:
    def test_set_start_date(self):

        settings = Settings()
        assert settings.start_date is None

        with pytest.raises(exceptions.DateException):
            settings.start_date = 'not-a-date'

        date = '2021/05/01'
        settings.start_date = date

        assert type(settings.start_date) is datetime.date
        assert settings.start_date.strftime('%Y/%m/%d') == date

    def test_set_end_date(self):

        settings = Settings()
        assert settings.end_date is None

        with pytest.raises(exceptions.DateException):
            settings.end_date = 'not-a-date'

        date = '2021/05/01'
        settings.end_date = date

        assert type(settings.end_date) is datetime.date
        assert settings.end_date.strftime('%Y/%m/%d') == date

    def test_tickers(self):
        settings = Settings()
        # Begin empty
        assert settings.tickers == []

        # remove unknown ticker or from empty should do nothing
        settings.remove_ticker('bbb')
        assert len(settings.tickers) == 0

        tickers = ['ccc', 'aaa', 'bbb']
        for ticker in tickers:
            settings.add_ticker(ticker)
        # duplicates should not exist
        settings.add_ticker('AAA')
        assert len(settings.tickers) == 3
        # tickers should be upper case and sorted
        assert settings.tickers == sorted([t.upper() for t in tickers])

        settings.remove_ticker('bbb')
        assert len(settings.tickers) == 2

        settings.clear_tickers()
        assert len(settings.tickers) == 0

    @utils.decorators.register_components
    def test_output_type(self):
        settings = Settings()
        assert settings.output_type is None

        with pytest.raises(exceptions.OutputTypeException):
            settings.output_type = "Invalid Type"

        # Test that the setter worked and didn't raise exception
        settings.output_type = aggregate_writer.output_type
        assert settings.output_type == aggregate_writer.output_type

    def test_output_path(self):
        settings = Settings()
        assert settings.output_path == settings.default_output_path

        with_fname_csv = './path/with/filename.csv'
        # TODO: This brings up a little problem, as in: we only check for csv
        # extension in the setter, so any other extensions would be considered
        # a path!
        with_fname_txt = './path/with/filename.txt'

        settings.output_path = with_fname_csv
        assert settings.output_path == with_fname_csv
        assert settings.path_with_filename is True

        settings.output_path = with_fname_txt
        assert settings.output_path == with_fname_txt
        assert settings.path_with_filename is True

    @utils.decorators.register_components
    def test_sources(self):
        settings = Settings()
        assert settings.sources == []

        # Test validation of values
        with pytest.raises(exceptions.SourceException):
            settings.add_source("UNKNOWN SOURCE")
        # Check that it's indeed empty
        assert settings.sources == []

        settings.add_source(finra.source)
        assert settings.sources == [finra.source]

        # Check for duplicate insertion, should not duplicate!
        settings.add_source(finra.source)
        assert settings.sources == [finra.source]

        # should do nothing when removing non-existing or non-present
        settings.remove_source("UNKNOWN SOURCE")
        assert settings.sources == [finra.source]

        settings.remove_source(finra.source)
        assert settings.sources == []

        for source in manager.get_sources():
            settings.add_source(source)
        assert settings.sources == sorted(manager.get_sources())

    def test_set_csv_dialect(self):
        settings = Settings()
        assert settings.csv_out_dialect == Settings.default_dialect

        with pytest.raises(exceptions.DialectException):
            settings.csv_out_dialect = "UNKNOWN DIALECT"

        # Try to set some dialects. it should not fail automatically
        # since validation is done through the manager itself
        for dialect in manager.get_dialects_list():
            settings.csv_out_dialect = dialect
            assert settings.csv_out_dialect == dialect

    @utils.decorators.register_components
    def test_load_fail_missing_file(self):
        wrong_path = './not/a/file.json'
        settings = Settings()

        with pytest.raises(exceptions.MissingFile):
            settings.from_file(wrong_path)
        assert settings.settings_loaded is False
        # Custom FileNotFound Exception
        assert settings.errors == [
            "Settings FILE not found at ./not/a/file.json"]

    @utils.decorators.register_components
    def test_load_fail_wrong_json(self):
        settings = Settings()

        path = os.path.join(mocks.constants.MOCKS_PATHS, 'options_wrong.json')
        with pytest.raises(exceptions.FileReadError):
            settings.from_file(path)
        assert settings.settings_loaded is False

    @utils.decorators.register_components
    def test_load_empty_json(self):
        path = os.path.join(mocks.constants.MOCKS_PATHS, 'options_empty.json')
        settings = Settings(path)
        settings.init()

        assert settings.start_date is None
        assert settings.output_type is None
        assert settings.output_path == settings.default_output_path
        assert settings.tickers == []

    @utils.decorators.register_components
    def test_load_settings_success(self):
        # Actually test loading mock options
        settings = Settings()
        assert settings.from_file(mocks.constants.SETTINGS_PATH) is True
        assert settings.settings_loaded is True

        # Validate the some fields are actually loaded
        validate_start_date(settings)
        assert settings.tickers == ['AMC', 'GME']
        assert settings.errors == []
        assert settings.output_type == ticker_writer.output_type

    @utils.decorators.register_components
    def test_settings_init(self):
        wrong_default_path = './not/a/file.json'
        settings = Settings(wrong_default_path)
        wrong_path_2 = "./another/wrong/path.json"
        expected_errors = [
            'Settings FILE not found at ./another/wrong/path.json',
            'Settings FILE not found at ./not/a/file.json'
        ]

        # should cause initialization with default values
        # (file not found or wrong)
        assert settings.init(wrong_path_2) is True
        assert settings.init_done is True
        assert settings.start_date is None
        assert settings.errors == expected_errors

        assert settings.init(mocks.constants.SETTINGS_PATH) is True
        assert settings.init_done is True
        validate_start_date(settings)

    @utils.decorators.register_components
    def test_settings_serialize(self):
        settings = Settings(mocks.constants.SETTINGS_PATH)

        assert settings.init() is True

        with open(mocks.constants.SETTINGS_PATH) as file:
            data = json.loads(file.read())
            out = settings.serialize()

            assert data == out

    @utils.decorators.register_components
    @utils.decorators.delete_file(mocks.constants.TEMP_JSON_FILE)
    def test_settings_tofile(self):

        settings = Settings(mocks.constants.SETTINGS_PATH)
        assert settings.init() is True

        settings.to_file(mocks.constants.TEMP_JSON_FILE)

        with open(mocks.constants.SETTINGS_PATH) as file:
            original = json.loads(file.read())

        with open(mocks.constants.TEMP_JSON_FILE) as file:
            out = json.loads(file.read())

        assert original == out

    @utils.decorators.register_components
    def test_init(self):
        # Test normal behaviour with a correct file
        s1 = Settings(mocks.constants.SETTINGS_PATH)
        s1.init()
        assert s1.init_done is True
        assert s1.start_date == utils.get_expected_start_date()
        # Test with wrong provided path but with a valid default one
        s2 = Settings("./not/a/path.json")
        s2.settings_path = mocks.constants.SETTINGS_PATH
        s2.init()
        assert s2.init_done is True
        assert s1.start_date == utils.get_expected_start_date()
        # Test with either files missing or wrong paths
        s3 = Settings("./not/a/path.json")
        s3.settings_path = "./default/not/path.json"
        s3.init()
        assert s3.init_done is True
        assert s3.start_date is None

    def test_set_defaults_no_components(self):
        # No components initialized, so 'from_file' should fail explicitly
        # and raise a bunch of exceptions
        with pytest.raises(exceptions.MissingSourceHandlersException):
            s = Settings(mocks.constants.SETTINGS_PATH)
            s.init()

        manager.register_handlers_from_obj(finra)
        with pytest.raises(exceptions.MissingWritersException):
            s = Settings(mocks.constants.SETTINGS_PATH)
            s.init()
