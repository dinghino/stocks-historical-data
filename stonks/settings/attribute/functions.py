from datetime import datetime
from scraper.settings import constants
# Default noop functions

def validator_always(*args, **kwargs):
    return true
def def_setter(inst, value):
    inst.value = value

# ListAttribute defaults

# Add value to the list of values avoiding duplicates
def def_adder(inst, value):
    if value not in inst.value:
        inst.value.append(value)

# Removes the value if is present
def def_remover(inst, value):
    try:
        inst.value.remove(value)
    except ValueError:
        pass
# Reset the value list to an empty list
def def_clearer(inst):
    inst.value.clear()

# DateAttribute functions

def date_setter(inst, datestr):
    for frmt in constants.VALID_DATES_FORMAT:
        try:
            inst.value = datetime.strptime(datestr, frmt).date()
            return True
        except ValueError:
            pass
    return False

# Custom functions
# TODO: Move into settings file

def add_source(inst, source):
    if not inst.validator.validate(source):
        raise inst.validator.Exception(source)
    if not source in inst.value:
        bisect.insort(inst.value, source)

def add_ticker(inst, ticker):
    ticker = ticker.upper()
    if (ticker in inst.value):
        return
    try:
        bisect.insort(inst.value, ticker)
    except:
        pass
