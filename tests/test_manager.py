import pytest
from scraper.components import manager, fetchers, parsers
from scraper.settings import constants

from tests import utils

@utils.decorators.manager_decorator
def test_handler_exceptions():
    # source exception
    with pytest.raises(TypeError):
        h = manager.Handler("NOT_VALID",fetchers.Finra, parsers.Finra)
    # fetcher exception
    with pytest.raises(TypeError):
        h = manager.Handler(constants.SOURCES.FINRA_SHORTS,utils.WrongClass, parsers.Finra)
    # parser exception
    with pytest.raises(TypeError):
        h = manager.Handler(constants.SOURCES.FINRA_SHORTS,fetchers.Finra, utils.WrongClass)


@utils.decorators.manager_decorator
def test_manager_registration():
    assert manager.registered_handler == []
    h = manager.register(constants.SOURCES.FINRA_SHORTS,fetchers.Finra, parsers.Finra)
    assert manager.registered_handler == [h]
    manager.register(constants.SOURCES.FINRA_SHORTS,fetchers.Finra, parsers.Finra)
    assert manager.registered_handler == [h]


@utils.decorators.manager_decorator
def test_manager_get_handler():
    handler = manager.register(constants.SOURCES.FINRA_SHORTS,fetchers.Finra, parsers.Finra)

    fetcher, parser = manager.get_handlers(constants.SOURCES.FINRA_SHORTS)
    assert handler.fetcher == fetcher
    assert handler.parser == parser
    with pytest.raises(Exception):
        manager.get_handlers(constants.SOURCES.SEC_FTD)
