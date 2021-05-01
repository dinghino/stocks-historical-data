from scraper.components.manager.handler_base import HandlerBase
from scraper.components.writers.base_writer import Writer
from scraper.settings.constants import OUTPUT_TYPE


class WriterHandler(HandlerBase):

    def __init__(self, type_, writer_cls):
        WriterHandler.validate_register(
            type_, OUTPUT_TYPE.VALID, "Output Type")
        WriterHandler.validate_component_class(
            writer_cls, Writer, "Writers")
        WriterHandler.validate_component_target(
            type_, writer_cls, "Writers")

        self.output_type = type_
        self.writer = writer_cls

    def __eq__(self, output_type):
        return self.output_type == output_type

    def __del__(self):
        self.writer and self.writer
        del self
