from stonks.components.manager.handler_base import HandlerBase
from stonks.components.base_writer import WriterBase


class WriterHandler(HandlerBase):

    def __init__(self, type_, writer_cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        WriterHandler.validate_component_class(
            type_, writer_cls, WriterBase, "Writer")

        self.output_type = type_
        self.writer = writer_cls

    def __repr__(self):
        return (
            f'<WriterHandler | {self.writer.__name__} for {self.output_type}>')
