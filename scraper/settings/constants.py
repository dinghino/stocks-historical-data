from scraper.settings import exceptions

VALID_DATES_FORMAT = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%y-%m-%d", "%y/%m/%d", ]

class FIELDS:
    START = "Start"
    END = "End"
    TYPE ="Type"
    PATH ="Path"
    TICKERS ="Tickers"
    SOURCES = "Sources"
    SETTINGS_PATH ="settings_path"
    CSV_DIALECT = "CSV Fmt"

class CONSTANTS:
    @classmethod
    def validate(cls, value):
        if not value in cls.VALID:
            raise cls.Exception(value)
        return True

class OUTPUT_TYPE(CONSTANTS):
    Exception = exceptions.OutputTypeException
    SINGLE_FILE = "Aggregate File"
    SINGLE_TICKER = "Individual Ticker files"
    VALID = [SINGLE_FILE, SINGLE_TICKER]

class SOURCES(CONSTANTS):
    Exception = exceptions.SourceException
    FINRA_SHORTS = "FINRA Short reports"
    SEC_FTD = "SEC FTDs"
    VALID = [FINRA_SHORTS, SEC_FTD]

class CSV_OUT_DIALECTS(CONSTANTS):
    Exception = exceptions.DialectException
    DEFAULT = "default"
    EXCEL = "excel"
    VALID = [DEFAULT, EXCEL]
