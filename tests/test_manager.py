import pytest
from scraper.components import manager, fetchers, parsers, writers
from scraper.settings import constants

from tests import utils

@utils.decorators.manager_decorator
def test_handler_exceptions():
    # source exception
    with pytest.raises(TypeError):
        h = manager.ProcessHandler("NOT_VALID",fetchers.Finra, parsers.Finra)
    # fetcher exception
    with pytest.raises(TypeError):
        h = manager.ProcessHandler(constants.SOURCES.FINRA_SHORTS,utils.WrongClass, parsers.Finra)
    # parser exception
    with pytest.raises(TypeError):
        h = manager.ProcessHandler(constants.SOURCES.FINRA_SHORTS,fetchers.Finra, utils.WrongClass)
    # writer out type
    with pytest.raises(TypeError):
        h = manager.WriterHandler("NOT VALID", writers.SingleFile)
    # writer class
    with pytest.raises(TypeError):
        h = manager.WriterHandler(constants.OUTPUT_TYPE.SINGLE_TICKER, utils.WrongClass)
    # invalid component for target
    with pytest.raises(TypeError):
        manager.ProcessHandler(constants.SOURCES.FINRA_SHORTS, fetchers.SecFtd, parsers.Finra)

@utils.decorators.manager_decorator
def test_manager_registration():
    assert manager.registered_handlers == []
    h = manager.register_handler(constants.SOURCES.FINRA_SHORTS,fetchers.Finra, parsers.Finra)
    assert manager.registered_handlers == [h]
    manager.register_handler(constants.SOURCES.FINRA_SHORTS,fetchers.Finra, parsers.Finra)
    assert manager.registered_handlers == [h]


@utils.decorators.manager_decorator
def test_manager_get_handler():
    handler = manager.register_handler(constants.SOURCES.FINRA_SHORTS,fetchers.Finra, parsers.Finra)

    fetcher, parser = manager.get_handlers(constants.SOURCES.FINRA_SHORTS)
    assert handler.fetcher == fetcher
    assert handler.parser == parser
    with pytest.raises(Exception):
        manager.get_handlers(constants.SOURCES.SEC_FTD)

@utils.decorators.manager_decorator
def test_manager_writers():
    assert manager.registered_writers == []
    handler = manager.register_writer(constants.OUTPUT_TYPE.SINGLE_FILE, writers.SingleFile)
    assert manager.registered_writers == [handler]

    with pytest.raises(Exception):
        manager.get_writer(constants.OUTPUT_TYPE.SINGLE_TICKER)
    
    assert manager.get_writer(constants.OUTPUT_TYPE.SINGLE_FILE) == handler.writer
