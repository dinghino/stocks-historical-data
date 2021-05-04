import os
import pytest
from stonks import App, Settings, exceptions
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
        assert app.settings.output_type is None
        assert app.settings.parse_rows is False
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
        app.select_handlers(handlers.finra.source)
        assert type(app.fetcher) == handlers.finra.Fetcher
        assert type(app.parser) == handlers.finra.Parser

        app.clear_handlers()
        assert_no_handlers()

        app.select_handlers(handlers.secftd.source)
        assert type(app.fetcher) == handlers.secftd.Fetcher
        assert type(app.parser) == handlers.secftd.Parser

    @utils.decorators.manager_decorator
    @utils.decorators.register_components
    def test_select_writer(self):

        app = getApp()

        assert app.settings.output_type == writers.ticker_writer.output_type
        app.select_writer()
        assert type(app.writer) is writers.ticker_writer.Writer

        app.settings.output_type = writers.aggregate_writer.output_type
        app.select_writer()
        assert type(app.writer) is writers.aggregate_writer.Writer

    @utils.decorators.manager_decorator
    def test_app_run_fail_no_sources(self):

        # The only wat to test this properly is to NOT init the settings
        # otherwise, if no source has been added to the manager it will throw
        # an error when loading the settings. this would simulate a full
        # execution but with no source set up in the settings json, while
        # having some components registered
        settings = Settings(mocks.constants.SETTINGS_PATH)
        app = App(settings)

        assert app.settings.sources == []

        with pytest.raises(exceptions.MissingSourcesException):
            for r in app.run():  # run is a generator!
                pass

    @utils.decorators.delete_file(*RUN_FULLPATHS)
    @utils.decorators.register_components
    def test_app_run(self):
        app = getApp()

        from pprint import pprint
        print(app.settings.serialize())


        # for done in app.run():
        #     assert done is True

        # outputs = [
        #     f for f in os.listdir(RUN_OUTPUT_DIR)
        #     if os.path.isfile(os.path.join(RUN_OUTPUT_DIR, f))
        # ]

        # assert outputs == RUN_FILENAMES
