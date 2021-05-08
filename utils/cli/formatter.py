import string
from termcolor import colored, COLORS


class formatter(string.Formatter):
    """ Custom formatter to use our syntax highlight formatting style for
    descriptions."""
    def get_colored_style(self, spec):
        c, s = spec, None
        try:
            c, s = spec.split("|")
            s = s.split(",")
        except Exception:
            pass
        # assuming correct colors are given, if _col_ is not in colors
        # we assume it's one (or list of) styling, especially if none are given
        if c not in COLORS.keys() and not s:
            s = c.split(',')
            c = None
        return (c, s)

    def get_value(self, key, args, kwargs):
        return key

    def format_field(self, value, format_spec=[]):
        col, style = self.get_colored_style(format_spec)
        value = colored(value, color=col, attrs=style)
        return super(formatter, self).format(value, format_spec)
