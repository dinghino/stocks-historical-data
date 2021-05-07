from stonks.constants import VALID_DATES_FORMAT  # noqa


class SettingsException(ValueError):
    def __str__(self):
        return self.message


class DateException(SettingsException):
    def __init__(self, datestr, field, *args, **kwargs):
        valid = ", ".join(VALID_DATES_FORMAT)
        self.message = "Could not parse {0} for '{1}'. Valid formats are: {2}"
        self.message = self.message.format(datestr, field, valid)


class OutputTypeException(SettingsException):
    def __init__(self, val, valid_list=[], *args, **kwargs):
        self.message = "OUTPUT value '{}' is invalid. should be one of '{}'"
        self.message = self.message.format(val, ", ".join(valid_list))


class SourceException(SettingsException):
    def __init__(self, val, valid_list=[], *args, **kwargs):
        self.message = "SOURCE value '{}' is invalid. should be one of '{}'"
        self.message = self.message.format(val, ", ".join(valid_list))


class DialectException(SettingsException):
    def __init__(self, val, valid_list=[], *args, **kwargs):
        self.message = "CSV FORMAT '{}' is invalid. should be one of '{}'"
        self.message = self.message.format(val, ", ".join(valid_list))


class MissingFile(SettingsException):
    def __init__(self, val, *args, **kwargs):
        self.message = 'Settings FILE not found at {}'.format(val)


class FileReadError(SettingsException):
    def __init__(self, val, *args, **kwargs):
        self.message = "Error while READING settings at {}".format(val)


class MissingSourcesException(Exception):
    def __init__(self):
        self.message = 'No Source is selected. Cannot run'


class MissingSourceHandlersException(Exception):
    def __init__(
            self,
            msg="Component manager has no source handlers registered"):
        self.message = msg


class MissingWritersException(Exception):
    def __init__(self):
        self.message = "Component manager writers registered"
