from scraper.settings import constants

class SettingsException(ValueError):
    def __str__(self):
        return self.message

class DateException(SettingsException):
    def __init__(self, datestr, field, *args, **kwargs):
        valid = ", ".join(constants.VALID_DATES_FORMAT)
        self.message = "Could not parse {0} for '{1}'. Valid formats are: {2}".format(
            datestr, field, valid)

class OutputTypeException(SettingsException):
    def __init__(self, val, *args, **kwargs):
        self.message = "OUTPUT value '{}' is invalid. should be one of '{}'".format(
            val, ", ".join(constants.OUTPUT_TYPE.VALID))

class SourceException(SettingsException):
    def __init__(self, val, *args, **kwargs):
        self.message = "SOURCE value '{}' is invalid. should be one of '{}'".format(
            val, ", ".join(constants.SOURCES.VALID))

class DialectException(SettingsException):
    def __init__(self, val, *args, **kwargs):
        self.message = "CSV DIALECT value '{}' is invalid. should be one of '{}'".format(
            val, ", ".join(constants.CSV_OUT_DIALECTS.VALID))

class MissingFile(SettingsException):
    def __init__(self, val, *args, **kwargs):
        self.message = 'Settings FILE not found at {}'.format(val)

class FileReadError(SettingsException):
    def __init__(self, val, *args, **kwargs):
        self.message = "Error while READING settings at {}".format(val)

