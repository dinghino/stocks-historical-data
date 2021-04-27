
class SettingsException(ValueError):

    def __str__(self):
        return self.message

class DateException(SettingsException):
    def __init__(self, datestr, field, *args):

        valid = ", ".join(valid_date_formats)
        self.message = "Could not parse {0} for '{1}'. Valid formats are: {2}".format(
            datestr, field, valid)
        # if args: self.message = args[0]
        # else: self.message = "There was an error while setting a date"

class OutputTypeException(SettingsException):
    def __init__(self, val, *args):
        self.message = "Provided value '{}' is not valid. should be one of '{}'".format(
            val, ", ".join(Settings.OUTPUT_TYPE.VALID))
    

class SourceException(SettingsException):
    def __init__(self, val, *args):
        self.message = "Provided value '{}' is not valid. should be one of '{}'".format(
            val, ", ".join(Settings.SOURCES.VALID))

class MissingFile(Exception):
    def __str__(self, val, *args):
        return 'Settings file not found at {}'.format(val)
