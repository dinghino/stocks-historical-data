import os
import pytest
from stonks import App, Settings, exceptions, manager, init as init_function
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


def test_app_init_success():
    manager.reset()
    done = init_function()
    assert done is True
    # Can't test for handlers presence or number since those are dynamically
    # included by the modules and can't test for module lenght.
    manager.reset()


def test_app_init_success_extra_objects():
    manager.reset()
    done = init_function(
        objects=[utils.FakeHandlerModule, utils.FakeWriterModule],
        skip_default=True)

    assert len(manager.get_all_handlers()) == 1
    assert len(manager.get_all_writers()) == 1

    assert done is True

    f, p = manager.get_handlers(utils.FakeHandlerModule.source)
    assert f == utils.FakeFetcher
    assert p == utils.FakeParser

    manager.reset()


@utils.decorators.manager_decorator
def test_app_init_success_extra_modules():
    # TODO: This should actually be a cal to is_xxx_module
    # But they both get out True. Need to find a way to fail this
    # assert manager.utils.is_writers_module(mocks.mod_writer) is False

    assert manager.utils.is_handlers_object(mocks.mod_handler) is True
    assert manager.utils.is_writer_object(mocks.mod_writer) is True

    # for our test they are both registered inside the module 'mocks'
    # so they get internally discriminated
    done = init_function(modules=mocks, skip_default=True)

    assert done is True

    w = manager.get_writer(utils.FakeWriterModule.output_type)
    assert w == utils.FakeWriter
    f, p = manager.get_handlers(utils.FakeHandlerModule.source)
    assert f == utils.FakeFetcher
    assert p == utils.FakeParser

    assert len(manager.get_all_handlers()) == 1
    assert len(manager.get_all_writers()) == 1


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

        for done in app.run():
            assert done is True

        outputs = [
            f for f in os.listdir(RUN_OUTPUT_DIR)
            if os.path.isfile(os.path.join(RUN_OUTPUT_DIR, f))
        ]

        assert outputs == RUN_FILENAMES
