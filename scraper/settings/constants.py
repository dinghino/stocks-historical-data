
VALID_DATES_FORMAT = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%y-%m-%d", "%y/%m/%d", ]

class FIELDS:
    START = "Start"
    END = "End"
    TYPE ="Type"
    PATH ="Path"
    TICKERS ="Tickers"
    SOURCES = "Sources"
    SETTINGS_PATH ="settings_path"

class OUTPUT_TYPE:
    SINGLE_FILE = "Aggregate File"
    SINGLE_TICKER = "Individual Ticker files"
    VALID = [SINGLE_FILE, SINGLE_TICKER]
    @staticmethod
    def validate(value):
        return value in OUTPUT_TYPE.VALID

class SOURCES:
    FINRA_SHORTS = "FINRA Short reports"
    SEC_FTD = "SEC FTDs"
    VALID = [FINRA_SHORTS, SEC_FTD]
    @staticmethod
    def validate(value):
        return value in SOURCES.VALID

class CSV_OUT_DIALECTS:
    DEFAULT = "default"
    EXCEL = "excel"
    VALID = [DEFAULT, EXCEL]
    @staticmethod
    def validate(value):
        return value in SOURCES.VALID
