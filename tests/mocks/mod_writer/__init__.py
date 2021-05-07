# from tests.utils import FakeWriter as Writer   # noqa
from stonks.components import WriterBase


class Writer(WriterBase):
    @staticmethod
    def is_for(): return 'test_output'

    def set_parse_rows(self): return True

    def write(self, header, data, source): return True


output_type = Writer.is_for()
friendly_name = Writer.is_for()
