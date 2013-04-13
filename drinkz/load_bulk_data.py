"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package
from . import recipes


def data_reader(fp):
    """
    Eliminates whitespace and commented lines

    Takes a file pointer.

    Is a generator wrapper around csv.reader

    Returns a list of records without whitespace or comments
    """
    try:
        reader = csv.reader(fp)
    except:
        db.FailedToReadCSV(Exception)
        
    x = []

    for x in reader:
        if (len(x) < 2):
            continue
        if ( not x[0].strip() ) or ( x[0].startswith('#') ):
            continue
        yield x

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    try:
        new_reader = data_reader(fp)
    except:
        db.DataReaderException(Exception)
        
    x = []
    n = 0

    for line in new_reader:
        if (len(line) != 3):
            continue
        try:
            (mfg, name, typ) = line
        except:
            db.InvalidFormatException(Exception)
        try:
            db.add_bottle_type(mfg, name, typ)
        except:
            db.FailedToAddBottle(Exception)
        n+=1

    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    try:
        new_reader = data_reader(fp)
    except:
        db.DataReaderException(Exception)
    
    x = []
    n = 0
    
    for line in new_reader:
        if (len(line) != 3): #data_reader needs to let recipe-> "a, b::50ml" through, which is two values
            continue
        try:
            (mfg, name, amount) = line
        except:
            db.InvalidFormatException(Exception)
        try:   
            db.add_to_inventory(mfg, name, amount)
        except:
            db.FailedToAddInventory(Exception)
        n+=1
    return n

def load_recipes(fp):
    """
    Loads in data of the recipe from a CSV file.

    Takes a file pointer.

    Adds data to database

    Returns number of records loaded.

    Note that a RecipeMissing exception is raised if recipes_db does not contain
    the name or type of recipe.
    """
    try:
        new_reader = data_reader(fp)
    except:
        db.DataReaderException(Exception)

    n = 0

    for line in new_reader:
        ingList = []
        try:
            recipeName = line[0]
            for ing in line[1:]: #Recipe will be slot 0, all ings will slots 1-n
                ingList.append(tuple(ing.split('::')))
        except:
            db.InvalidFormatException(Exception)
        try:
            recipe = recipes.Recipe(recipeName, ingList)
            db.add_recipe( recipe )
        except:
            db.FailedToAddRecipes(Exception)
        n+=1
    return n
