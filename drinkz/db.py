"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = []
_inventory_db = []

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set()
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class FailedToAddBottle(Exception):
    pass

class FailedToAddInventory(Exception):
    pass

class DataReaderException(Exception):
    pass

class FailedToReadCSV(Exception):
    pass

class InvalidFormatException(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    if (mfg, liquor) in _inventory_db:

        if ( amount[-2:] == 'oz' ):
            amount = float( amount.strip('oz') )
            amount *= 29.5735
            _inventory_db[(mfg, liquor)] += amount
        elif ( amount[-2:] == 'ml' ):
            amount = float( amount.strip('ml'))
            _inventory_db[(mfg,liquor)] += amount
    else:
        if ( amount[-2:] == 'oz' ):
            amount = float( amount.strip('oz') )
            amount *= 29.5735
            _inventory_db[(mfg, liquor)] = amount
        elif ( amount[-2:] == 'ml' ):
            amount = float( amount.strip('ml'))
            _inventory_db[(mfg,liquor)] = amount

def check_inventory(mfg, liquor):
    for key in _inventory_db.keys():
        if mfg == key[0] and liquor == key[1]:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    total = 0
    if ( (mfg,liquor) in _inventory_db ):
        total = _inventory_db.get((mfg,liquor))            
        total = str(total) + " ml"
    return total

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db.keys():
        yield key[0], key[1]
