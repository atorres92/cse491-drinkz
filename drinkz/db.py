"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipe_db = {}
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

def add_recipe(r):
    _recipe_db[r.name] = r
    
def get_recipe(name):
    if name in _recipe_db.values():
        return recipe_db.get(name)
    
def get_all_recipes():
    for values in _recipe_db.values():
        valueList.append(values)
    return valueList

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def convert_to_ml(amt):
    if amt[-2:] == 'ml':
        amtNum = float(amt.strip('ml'))
    elif amt[-2:] == 'oz':
        amtNum = float(amt.strip('oz'))
        amtNum *= 29.5735
    elif amt[-5:] == 'liter':
        amtNum = float(amt.strip('liter'))
        amtNum *= 1000
    elif amt[-6:] == 'gallon':
        amtNum = float(amt.strip('gallon'))
        amtNum *= 3785.41
    else:
        amtNum = '0 ml'
    return amtNum

def check_recipe_needs(ing):
    for (m, l, t) in _bottle_types_db:
        if ing[0] == m or ing[0] == l or ing[0] == t:
            amtNeeded = convert_to_ml(ing[1])
            currAmount = db.get_liquor_amount(m,l)
            if amtNeeded > currAmount:
                return [(ing[0], (amtNeeded - currAmount))] 
            else:
                return [(ing[0], 0)]
        else:
            return [(ing[0], ing[1])]

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    amount = convert_to_ml(amount)
    
    if (mfg,liquor) in _inventory_db:
        _inventory_db[(mfg,liquor)] += amount
    else:
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
        #total = str(total) + " ml" 
    return total

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db.keys():
        yield key[0], key[1]
