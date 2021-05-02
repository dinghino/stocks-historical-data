import os
import pytest
from stonks import App, Settings, constants, exceptions
from stonks.components import handlers, writers
from tests import mocks, utils


def getApp(init=True):
    settings = Settings(mocks.constants.SETTINGS_PATH)
    if init:
        settings.init()
    return App(settings)


RUN_FILENAMES = [
    "20210427-20210427_SEC_FTD_AMC.csv",
    "20210427-20210427_SEC_FTD_GME.csv"
]
RUN_OUTPUT_DIR = os.path.join(mocks.constants.MOCKS_PATHS, 'output')
RUN_FULLPATHS = [os.path.join(RUN_OUTPUT_DIR, f) for f in RUN_FILENAMES]


class TestApp:
    def test_default(self):
        app = getApp(init=False)
        assert app.settings.output_type == constants.OUTPUT_TYPE.SINGLE_TICKER
        assert app.parse_rows is False
        assert app.settings.start_date is None

    @utils.decorators.manager_decorator
    @utils.decorators.register_components
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
        assert type(app.fetcher) == handlers.finra.Fetcher
        assert type(app.parser) == handlers.finra.Parser

        app.clear_handlers()
        assert_no_handlers()

        app.select_handlers(constants.SOURCES.SEC_FTD)
        assert type(app.fetcher) == handlers.secftd.Fetcher
        assert type(app.parser) == handlers.secftd.Parser

    @utils.decorators.manager_decorator
    @utils.decorators.register_components
    def test_select_writer(self):

        app = getApp()

        assert app.settings.output_type == constants.OUTPUT_TYPE.SINGLE_TICKER
        app.select_writer()
        assert type(app.writer) is writers.MultiFile

        app.settings.output_type = constants.OUTPUT_TYPE.SINGLE_FILE
        app.select_writer()
        assert type(app.writer) is writers.SingleFile

    # @utils.decorators.register_components
    def test_app_run_fail_no_sources(self):
        app = getApp()
        for s in app.settings.sources:
            app.settings.remove_source(s)

        assert app.settings.sources == []

        with pytest.raises(exceptions.MissingSourcesException):
            for r in app.run():  # run is a generator!
                pass

    @utils.decorators.delete_file(*RUN_FULLPATHS)
    @utils.decorators.register_components
    def test_app_run(self):
        app = getApp()
        for done in app.run():
            assert done is True

        outputs = [
            f for f in os.listdir(RUN_OUTPUT_DIR)
            if os.path.isfile(os.path.join(RUN_OUTPUT_DIR, f))
        ]

        assert outputs == RUN_FILENAMES
