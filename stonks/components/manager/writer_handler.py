from stonks.components.manager.handler_base import HandlerBase
from stonks.components.base_writer import WriterBase
from stonks.constants import OUTPUT_TYPE


class WriterHandler(HandlerBase):

    def __init__(self, type_, writer_cls):
        WriterHandler.validate_register(
            type_, OUTPUT_TYPE.VALID, "Output Type")
        WriterHandler.validate_component_class(
            writer_cls, WriterBase, "Writers")
        WriterHandler.validate_component_target(
            type_, writer_cls, "Writers")

        self.output_type = type_
        self.writer = writer_cls

    def __repr__(self):
        return f'<WriterHandler | {self.writer.__name__} for {self.output_type}>'  # noqa
