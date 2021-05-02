# NOTE:
# This is a test file that SHOULD NOT BE COMMITTED
# To test an implementation of an attribute class to slim the settings class
# and ensure more safety on the settings value, allowing each value to be
# self handled
import bisect
from datetime import datetime
from scraper.settings import constants, exceptions
from . import functions

class Attribute:
    def __init__(self,
        name,
        default,
        setter=functions.def_setter,
        validator=functions.validator_always,
    ):
        self.value = default
        self.name = name
        self.setter = setter
        self.validator = validator
        
    def __get__(self, inst, owner):
        return self.value

    def __set__(self, value, inst, owner):
        if self.validator(value):
            self.setter(self, value)

class DateAttribute(Attribute):
    def __init__(self,
        name,
        default=None,
        setter=functions.date_setter,
        validator=functions.validator_always,
    ):
        super().__init__(name=name, default=default, setter=setter, validator=validator)
        self.exception = exceptions.DateException

    def __set__(self, instance, value):
        if not self.setter(self, value):
            raise self.exception(value, self.name);

class ListAttribute(Attribute):
    def __init__(self,
        name,
        default = [],
        setter=functions.def_setter,
        validator=functions.validator_always,
        adder=functions.def_adder,
        remover=functions.def_remover,
        clearer=functions.def_clearer,
    ):
        super().__init__(name=name, default=default, setter=setter, validator=validator)

        self.adder = adder
        self.remover = remover
        self.clearer = clearer

    def add(self, value):
        self.adder(self, value)
    def remove(self, value):
        self.remover(self, value) 
    def clear(self):
        self.clearer(self)

class Settings:

    _start_date = DateAttribute(name=constants.FIELDS.START, default=None)
    _end_date = DateAttribute(name=constants.FIELDS.END, default=None)
    _tickers = ListAttribute(name=constants.FIELDS.TICKERS, adder=functions.add_ticker)
    _sources = ListAttribute(name=constants.FIELDS.SOURCES, validator=constants.SOURCES, adder=functions.add_source)
    _outpu_type = ListAttribute(name=constants.FIELDS.TYPE, validator=constants.OUTPUT_TYPE)
    _output_path = Attribute(name=constants.FIELDS.PATH, default="./")
    _csv_out_dialect = Attribute(name=constants.FIELDS.CSV_DIALECT, default='excel', validator=constants.CSV_OUT_DIALECTS)

    def __init__(self):
        pass
    @property
    def start_date(self):
        return self._start_date.get
    @property
    def end_date(self):
        return self._end_date.get
    @property
    def tickers(self):
        return self._tickers.get
    @property
    def sources(self):
        return self._sources.get
    @property
    def outpu_type(self):
        return self._outpu_type.get
    @property
    def output_path(self):
        return self._output_path.get
    @property
    def csv_out_dialect(self):
        return self._csv_out_dialect.get



s = Settings()


# ============================================================================

class Attr:
    val = [1]
    def __get__(self, parent, cls, *args, **kwargs):
        print(self, parent, cls, args, kwargs)
        return self.val

    def __getattr__(self, key):
        return getattr(self, key, 'v')

    def add(self, v):
        val.append(v)

class A:
    v = Attr()


a = A()
