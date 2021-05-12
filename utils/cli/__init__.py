from .formatter import formatter as _formatter  # noqa
from .functions import (echo_divider, get_terminal_size, highlight,  # noqa
                        terminal_width)

format = _formatter().format
