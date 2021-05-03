import csv
import pytest
from stonks.components import manager, handlers, writers

from tests import utils
from tests.mocks import fake_handlers_module, fake_writers_module


@utils.decorators.manager_decorator
def test_handler_exceptions():
    # source exception
    with pytest.raises(TypeError):
        manager.SourceHandler(
            "NOT_VALID",
            handlers.finra.Fetcher,
            handlers.finra.Parser,
            handlers.finra.filename_appendix)
    # fetcher exception
    with pytest.raises(TypeError):
        manager.SourceHandler(
            handlers.finra.source, utils.WrongClass,
            handlers.finra.Parser, handlers.finra.filename_appendix)
    # parser exception
    with pytest.raises(TypeError):
        manager.SourceHandler(
            handlers.finra.source, handlers.finra.Fetcher,
            utils.WrongClass, handlers.finra.filename_appendix)
    # writer out type
    with pytest.raises(TypeError):
        manager.WriterHandler("NOT VALID", writers.ticker_writer.Writer)
    # writer class
    with pytest.raises(TypeError):
        manager.WriterHandler("nope", utils.WrongClass)
    # invalid component for target
    with pytest.raises(TypeError):
        manager.SourceHandler(
            handlers.finra.source, handlers.secftd.Fetcher,
            handlers.finra.Parser, handlers.finra.filename_appendix)


@utils.decorators.manager_decorator
def test_manager_registration():
    assert manager.get_all_handlers() == []
    h = manager.register_handler(
        handlers.finra.source, handlers.finra.Fetcher,
        handlers.finra.Parser, handlers.finra.filename_appendix)
    assert manager.get_all_handlers() == [h]
    # test duplication of handler
    manager.register_handler(
        handlers.finra.source, handlers.finra.Fetcher,
        handlers.finra.Parser, handlers.finra.filename_appendix)
    assert manager.get_all_handlers() == [h]


@utils.decorators.manager_decorator
def test_manager_get_handler():
    handler = manager.register_handler(
        handlers.finra.source, handlers.finra.Fetcher,
        handlers.finra.Parser, handlers.finra.filename_appendix)

    fetcher, parser = manager.get_handlers(handlers.finra.source)
    assert handler.fetcher == fetcher
    assert handler.parser == parser
    with pytest.raises(Exception):
        manager.get_handlers(handlers.secftd.source)


@utils.decorators.manager_decorator
def test_manager_writers():
    assert manager.get_all_writers() == []
    handler = manager.register_writer(
        writers.aggregate_writer.output_type,
        writers.aggregate_writer.Writer)

    assert manager.get_all_writers() == [handler]

    with pytest.raises(Exception):
        manager.get_writer('nope')

    assert manager.get_writer(
        writers.aggregate_writer.output_type) == handler.writer


@utils.decorators.manager_decorator
def test_manager_dialects():
    assert manager.get_dialects() == ()
    manager.register_dialect('test', delimiter='|')

    assert 'test' in csv.list_dialects()

    # duplicates not allowed by name
    with pytest.raises(ValueError):
        manager.register_dialect('test', delimiter=',')

    assert manager.get_dialects() == (('test', {'delimiter': '|'}), )

    registered = manager.get_dialects_list()
    csv_registered = csv.list_dialects()
    assert len(registered) == len(csv_registered)
    for d in csv_registered:
        assert d in registered

    manager.reset()
    assert manager.get_dialects() == ()


@utils.decorators.manager_decorator
def test_dialects_bulk_registration():
    assert manager.csv_dialects == []
    assert manager.handlers == []

    test_dialects = [('test', {'delimiter': '$'})]

    manager.register_dialects_from_list(test_dialects)

    # test duplicated dialect registration
    with pytest.raises(ValueError):
        manager.register_dialects_from_list(test_dialects)

    assert len(manager.csv_dialects) == 1
    assert manager.csv_dialects[0]['name'] == 'test'


@utils.decorators.manager_decorator
def test_handlers_bulk_registration():
    # Test handlers registration from modules
    manager.register_handlers_from_modules(fake_handlers_module)
    manager.register_writers_from_module(fake_writers_module)

    assert len(manager.handlers) == 2

    # Test handlers from random class/object
    class FakeHandlerStorage:
        Fetcher = handlers.secftd.Fetcher
        Parser = handlers.secftd.Parser
        source = handlers.secftd.source

    manager.register_handlers_from_obj(FakeHandlerStorage)
    assert len(manager.handlers) == 3

    f, p = manager.get_handlers(handlers.secftd.source)
    assert f == handlers.secftd.Fetcher
    assert p == handlers.secftd.Parser

    # module with missing source should be skipped. That attribute acts as
    # an activator and validator against the classes
    class MissingSource:
        Fetcher = handlers.secftd.Fetcher
        Parser = handlers.secftd.Parser

    manager.register_handlers_from_obj(FakeHandlerStorage)
    assert len(manager.handlers) == 3

    # test mismatch on manager.utils is_handler failing registration
    class WrongCouple:
        Fetcher = handlers.secftd.Fetcher
        Parser = handlers.finra.Parser
        source = 'test_source'  # whatever for the test

    with pytest.raises(TypeError):
        manager.register_handlers_from_obj(WrongCouple)

    assert len(manager.handlers) == 3

    # Wrong types on attributes, missing required attributes
    class WrongEverything:
        Fetcher = []
        derp = []
        source = 'test_source'

    with pytest.raises(TypeError):
        manager.register_handlers_from_obj(WrongEverything)

    assert len(manager.handlers) == 3
