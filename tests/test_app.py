from scraper import App
from scraper.settings import Settings, constants
from scraper.components import fetchers, parsers, writers, manager
from tests import mocks, utils


def getApp(init=True):
    settings = Settings(mocks.constants.SETTINGS_PATH)
    if init:
        settings.init()
    return App(settings)


def register_components():
    manager.register_handler(
        constants.SOURCES.FINRA_SHORTS, fetchers.Finra, parsers.Finra)
    manager.register_handler(
        constants.SOURCES.SEC_FTD, fetchers.SecFtd, parsers.SecFtd)
    manager.register_writer(
        constants.OUTPUT_TYPE.SINGLE_FILE, writers.SingleFile)
    manager.register_writer(
        constants.OUTPUT_TYPE.SINGLE_TICKER, writers.MultiFile)


class TestApp:
    def test_default(self):
        app = getApp(init=False)
        assert app.settings.output_type == constants.OUTPUT_TYPE.SINGLE_TICKER
        assert app.parse_rows is False
        assert app.settings.start_date is None

    @utils.decorators.manager_decorator
    def test_select_main_components(self):
        def assert_no_handlers():
            assert app.fetcher is None
            assert app.parser is None

        register_components()

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

    @utils.decorators.manager_decorator
    def test_select_writer(self):

        app = getApp()

        register_components()

        assert app.settings.output_type == constants.OUTPUT_TYPE.SINGLE_TICKER
        app.select_writer()
        assert type(app.writer) is writers.MultiFile

        app.settings.output_type = constants.OUTPUT_TYPE.SINGLE_FILE
        app.select_writer()
        assert type(app.writer) is writers.SingleFile
