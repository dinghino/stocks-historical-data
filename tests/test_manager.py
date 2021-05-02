import csv
import pytest
from stonks.components import manager, fetchers, parsers, writers
from stonks import constants

from tests import utils


@utils.decorators.manager_decorator
def test_handler_exceptions():
    # source exception
    with pytest.raises(TypeError):
        manager.SourceHandler(
            "NOT_VALID", fetchers.Finra, parsers.Finra)
    # fetcher exception
    with pytest.raises(TypeError):
        manager.SourceHandler(
            constants.SOURCES.FINRA_SHORTS, utils.WrongClass, parsers.Finra)
    # parser exception
    with pytest.raises(TypeError):
        manager.SourceHandler(
            constants.SOURCES.FINRA_SHORTS, fetchers.Finra, utils.WrongClass)
    # writer out type
    with pytest.raises(TypeError):
        manager.WriterHandler(
            "NOT VALID", writers.SingleFile)
    # writer class
    with pytest.raises(TypeError):
        manager.WriterHandler(
            constants.OUTPUT_TYPE.SINGLE_TICKER, utils.WrongClass)
    # invalid component for target
    with pytest.raises(TypeError):
        manager.SourceHandler(
            constants.SOURCES.FINRA_SHORTS, fetchers.SecFtd, parsers.Finra)


@utils.decorators.manager_decorator
def test_manager_registration():
    assert manager.get_all_handlers() == []
    h = manager.register_handler(
        constants.SOURCES.FINRA_SHORTS, fetchers.Finra, parsers.Finra)
    assert manager.get_all_handlers() == [h]
    # test duplication of handler
    manager.register_handler(
        constants.SOURCES.FINRA_SHORTS, fetchers.Finra, parsers.Finra)
    assert manager.get_all_handlers() == [h]


@utils.decorators.manager_decorator
def test_manager_get_handler():
    handler = manager.register_handler(
        constants.SOURCES.FINRA_SHORTS, fetchers.Finra, parsers.Finra)

    fetcher, parser = manager.get_handlers(constants.SOURCES.FINRA_SHORTS)
    assert handler.fetcher == fetcher
    assert handler.parser == parser
    with pytest.raises(Exception):
        manager.get_handlers(constants.SOURCES.SEC_FTD)


@utils.decorators.manager_decorator
def test_manager_writers():
    assert manager.get_all_writers() == []
    handler = manager.register_writer(
        constants.OUTPUT_TYPE.SINGLE_FILE, writers.SingleFile)
    assert manager.get_all_writers() == [handler]

    with pytest.raises(Exception):
        manager.get_writer(
            constants.OUTPUT_TYPE.SINGLE_TICKER)

    assert manager.get_writer(
        constants.OUTPUT_TYPE.SINGLE_FILE) == handler.writer


@utils.decorators.manager_decorator
def test_manager_dialects():
    assert manager.get_dialects() == ()
    manager.register_dialect('test', delimiter='|')

    assert 'test' in csv.list_dialects()

    # duplicates not allowed by name
    with pytest.raises(ValueError):
        manager.register_dialect('test', delimiter=',')

    assert manager.get_dialects() == (('test', {'delimiter': '|'}), )

    assert manager.get_dialects_list() == ('test',)

    manager.reset()
    assert manager.get_dialects() == ()
