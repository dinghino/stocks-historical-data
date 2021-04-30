import pytest
from datetime import datetime
from scraper import App
from scraper.settings import Settings, constants
from scraper.components import fetchers, parsers, writers
from tests import mocks, utils

def getApp(init=True):
    settings = Settings(mocks.constants.SETTINGS_PATH)
    if init:
        settings.init()
    return App(settings)

class TestApp:
    def test_default(self):
        app = getApp(init=False)
        assert app.settings.output_type == constants.OUTPUT_TYPE.SINGLE_TICKER
        assert app.parse_rows is False
        assert app.settings.start_date == None

    def test_select_main_components(self):
        def assert_no_handlers():
            assert app.fetcher is None
            assert app.parser is None

        app = getApp()
        utils.get_expected_start_date()
        assert_no_handlers()
        # NOTE: For now i can't find a way to test all the sources, so we'll do
        # one or two instead
        app.select_handlers(constants.SOURCES.FINRA_SHORTS)
        assert type(app.fetcher) == fetchers.Finra
        assert type(app.parser) == parsers.Finra

        app.clear_handlers()
        assert_no_handlers()

        app.select_handlers(constants.SOURCES.SEC_FTD)
        assert type(app.fetcher) == fetchers.SecFtd
        assert type(app.parser) == parsers.SecFtd

    def test_select_writer(self):

        app = getApp()
        assert app.settings.output_type == constants.OUTPUT_TYPE.SINGLE_TICKER
        app.select_writer()
        assert type(app.writer) is writers.MultiFile

        app.settings.output_type = constants.OUTPUT_TYPE.SINGLE_FILE
        app.select_writer()
        assert type(app.writer) is writers.SingleFile
