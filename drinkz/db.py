"""
Database functionality for drinkz information.
_bottle_types_db is a set because they are just elements of items
_inventory_db is a dictionary because each inventory item will have a value, that is, the amount of liquor for that specific (mfg,liquor)
_recipe_db is a dict as well because the name will be the key, and the recipe for that name will be the value of the dict

"""

import convert

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipe_db = {}
def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipe_db = {}

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

class DuplicateRecipeName(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def add_recipe(r):
    if ( r.get_name() in _recipe_db ):
        raise DuplicateRecipeName
    _recipe_db[r.get_name()] = r
    
def get_recipe(name):
    if name in _recipe_db.keys():
        return _recipe_db.get(name)
    
def get_all_recipes():
    valueList = []
    for values in _recipe_db.values():
        valueList.append(values)
    return valueList

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def check_inventory_for_type(typ):
    b_list = []
    for bottle in _bottle_types_db:
        if typ in bottle:
            b_list.append((bottle[0], bottle[1]))

    return b_list

def check_recipe_needs(ing):
    amtNeeded = convert.convert_to_ml(ing[1])
    bottlesMatch = check_inventory_for_type(ing[0])
    amtList = []
    for bottle in bottlesMatch:
        amtList.append(get_liquor_amount(bottle[0],bottle[1]))
    amtList.sort()
    if len(amtList) > 0:
        currAmount = amtList[-1]
        if amtNeeded > currAmount:
            return (ing[0], (amtNeeded - currAmount))
        else:
            return (ing[0], 0)
    else:
        return (ing[0], amtNeeded)

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    amount = convert.convert_to_ml(amount)
    
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
