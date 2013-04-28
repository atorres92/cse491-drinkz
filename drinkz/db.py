"""
Database functionality for drinkz information.
_bottle_types_db is a set because they are just elements of items
_inventory_db is a dictionary because each inventory item will have a value, that is, the amount of liquor for that specific (mfg,liquor)
_recipe_db is a dict as well because the name will be the key, and the recipe for that name will be the value of the dict

"""

import convert
import sqlite3
import recipes
import os
from cPickle import dump, load

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    try:
        #sqlite3.register_converter("json", json.loads)
        
        conn = sqlite3.connect("tables.db")

        cursor = conn.cursor()
        
        cursor.execute('''DROP TABLE IF EXISTS bottletypes''')
        cursor.execute('''DROP TABLE IF EXISTS inventory''')
        cursor.execute('''DROP TABLE IF EXISTS recipe''')
        cursor.execute('''DROP TABLE IF EXISTS fooddrinkz''')
        
        cursor.execute('''CREATE TABLE bottletypes(Id INTEGER PRIMARY KEY, liquor TEXT, mfg TEXT, typ TEXT)''')
        cursor.execute('''CREATE TABLE inventory(Id INTEGER PRIMARY KEY, liquor TEXT, mfg TEXT, amount FLOAT)''')
        cursor.execute('''CREATE TABLE recipe(Id INTEGER PRIMARY KEY, name TEXT, ingredients TEXT)''')
        cursor.execute('''CREATE TABLE fooddrinkz(Id INTEGER PRIMARY KEY, food TEXT, drinkz TEXT)''')
        
        conn.commit()
        
    except sqlite3.Error, e:
        print "bad table!"
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
            
#FOOD_DRINKZ SQLITE#
def db_fooddrinkz_insert(food, drinkz):
    conn = sqlite3.connect("tables.db")
    
    #food stored in database as string
    #drinkz stored in database as list, like so: "drink1\ndrink2\ndrink3\n..."
    
    drinks = ""
    
    #food ex: 'Chicken'
    #drinkz ex: ['drink1', 'drink2', 'drink3']
    
    for drink in drinkz:
        drinks += drink + "\n"
        
    try:
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO fooddrinkz(food,drinkz) VALUES(?, ?)", (food,drinks,))        
        conn.commit()
        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
            
def db_fooddrinkz_checkexists(food, drinkz):
    conn = sqlite3.connect("tables.db")

    drinks = ""

    for drink in drinkz:
        drinks += drink + "\n"

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT food,drinkz FROM fooddrinkz WHERE food = ? AND drinkz = ?", (food,drinks,))        
        conn.commit()
        
        rows =  cursor.fetchall()
        
        if (len(rows) == 0):
            return False
        else:
            return True
                
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
            
def db_fooddrinkz_getall():
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT food,drinkz FROM fooddrinkz")        
        conn.commit()        

        b_list = []

        while True:
            row =  cursor.fetchone()
            d_list = []
            
            if row == None:
                break
            
            b_list.append((str(row[0]),str(row[1]).splitlines()))
        return b_list
                        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
    
#BOTTLE_TYPES SQLITE#
def db_bottletypes_insert(mfg, liquor, typ):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO bottletypes(mfg,liquor,typ) VALUES(?, ?, ?)", (mfg,liquor,typ,))        
        conn.commit()
        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
            

def db_bottletypes_checkexists(mfg, liquor):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT mfg,liquor FROM bottletypes WHERE mfg = ? AND liquor = ?", (mfg,liquor,))        
        conn.commit()
        
        rows =  cursor.fetchall()
        
        if (len(rows) == 0):
            return False
        else:
            return True
                
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()

def db_bottletypes_checkfortype(typ):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT mfg,liquor FROM bottletypes WHERE typ = ?", (typ,))        
        conn.commit()        

        b_list = []

        while True:
            row =  cursor.fetchone()
            
            if row == None:
                break
            
            b_list.append((str(row[0]),str(row[1])))
        return b_list
                        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()    
            
def db_bottletypes_getall():
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT mfg,liquor FROM bottletypes")        
        conn.commit()        

        b_list = []

        while True:
            row =  cursor.fetchone()
            
            if row == None:
                break
            
            b_list.append((str(row[0]),str(row[1])))
        return b_list
                        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()      
            
#INVENTORY SQLITE      
def db_inventory_insert(mfg, liquor, amount):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO inventory(mfg,liquor,amount) VALUES(?, ?, ?)", (mfg,liquor,amount,))        
        conn.commit()
        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
            
def db_inventory_update(mfg, liquor, amount):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("UPDATE inventory SET amount = amount + ? WHERE mfg = ? AND liquor = ?", (amount,mfg,liquor))
        conn.commit()
        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
            
def db_inventory_getamount(mfg, liquor):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT amount FROM inventory WHERE mfg = ? AND liquor = ?", (mfg,liquor,))        
        conn.commit()
        
        rows =  cursor.fetchall()
        
        if (len(rows) == 0):
            return 0
        else:
            return rows[0][0]
                
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()  
            
def db_inventory_check(mfg,liquor):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT amount FROM inventory WHERE mfg = ? AND liquor = ?", (mfg,liquor,))        
        conn.commit()
        
        rows =  cursor.fetchall()
        
        if (len(rows) == 0):
            return False
        else:
            return True
                
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close() 
            
def db_inventory_getall():
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT mfg,liquor FROM inventory")        
        conn.commit()
        
        b_list = []

        while True:
            row =  cursor.fetchone()
            
            if row == None:
                break
            
            b_list.append((str(row[0]),str(row[1])))
        return b_list
                
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close() 
                               
#RECIPE SQLITE                       
def db_recipe_insert(name, ingredients):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO recipe(name, ingredients) VALUES(?, ?)", (name,ingredients,))        
        conn.commit()
        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
            
def db_recipe_getrecipe(name):
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ingredients FROM recipe WHERE name = ?", (name,) )        
        conn.commit()
        
        b_list = []

        while True:
            row =  cursor.fetchone()
            
            if row == None:
                break
            
            for ingr in row:
                strIngr = str(ingr)
                tup = strIngr.splitlines()
                for item in tup:
                    itemSpl = tuple(item.split('::'))
                    b_list.append(itemSpl)
            
            recipe = recipes.Recipe(name, b_list)
            
            return recipe
        return False

        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()
            
def db_recipe_getall():
    conn = sqlite3.connect("tables.db")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name,ingredients FROM recipe" )        
        conn.commit()
        
        r_list = []
        
        while True:
            b_list = []
            row =  cursor.fetchone()
            
            if row == None:
                break
            
            strName = str(row[0])
                        
            for ingr in row[1:]:
                strIngr = str(ingr)
                tup = strIngr.splitlines()
                for item in tup:
                    itemSpl = tuple(item.split('::'))
                    b_list.append(itemSpl)
            
            recipe = recipes.Recipe(strName, b_list)
            r_list.append(recipe)
        return r_list

        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if conn:
            conn.close()    
                
#END SQLITE#
                        
def save_db(filename):
    con = sqlite3.connect('tables.db')
    with open(filename,'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)
    f.close()
    """
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipe_db)
    dump(tosave, fp)

    fp.close()
    """
def load_db(filename):
    
    try:
        os.remove('tables.db')
    except OSError:
        pass
    con = sqlite3.connect('tables.db')
    f = open(filename,'r')
    sql = f.read()
    cur = con.cursor()
    cur.executescript(sql)
    f.close()
    
    """
    global _bottle_types_db, _inventory_db, _recipe_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipe_db) = loaded
    
    fp.close()
    """

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class FailedToAddBottle(Exception):
    pass

class FailedToAddInventory(Exception):
    pass

class FailedToAddRecipes(Exception):
    pass

class FailedToAddFooddrinkz(Exception):
    pass

class DataReaderException(Exception):
    pass

class FailedToReadCSV(Exception):
    pass

class InvalidFormatException(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

class DuplicateFoodDrinkz(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    
    db_bottletypes_insert(mfg,liquor,typ)
    
    #_bottle_types_db.add((mfg, liquor, typ))
    
def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    amount = convert.convert_to_ml(amount)
    
    if check_inventory(mfg,liquor):
        db_inventory_update(mfg,liquor,amount)
    else:
        db_inventory_insert(mfg,liquor,amount)
        
def add_recipe(r):
    if ( get_recipe(r.get_name()) ):
        raise DuplicateRecipeName
    
    db_recipe_insert( r.get_name(), r.get_ingredientsStr() )
    
def add_fooddrinkz(food, drinkz):
    if ( db_fooddrinkz_checkexists(food,drinkz) ):
        raise DuplicateFoodDrinkz
    db_fooddrinkz_insert(food, drinkz)
    
def check_fooddrinks(food,drinkz):
    return db_fooddrinkz_checkexists(food,drinkz)
    
def get_all_fooddrinkz(): 
    return db_fooddrinkz_getall()

def get_recipe(name):
    result = db_recipe_getrecipe(name)
    return result

def check_inventory(mfg, liquor):
    return db_inventory_check(mfg,liquor)
    
def get_all_recipes():
    valueList = []
    valueList = db_recipe_getall()
    print valueList
    return valueList

def get_all_bottle_types():
    return db_bottletypes_getall()

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    inv_list = db_inventory_getall()
    for key in inv_list:
        yield key[0], key[1]
        
def _check_bottle_type_exists(mfg, liquor):
    return db_bottletypes_checkexists(mfg,liquor)
        
def get_usable_recipes():
    usable_recipes = []
    ingredients_needed = []
    
    for recipe in get_all_recipes():
        print "start"
        print recipe.get_name()
        numIng = len(recipe.get_ingredients())
        currHav = 0
        print recipe.get_ingredients()
        for ingredient in recipe.get_ingredients():
            #print ingredient
            if ( check_recipe_needs(ingredient)[1] == 0 ):
                currHav+=1
        if (currHav == numIng):
            usable_recipes.append(recipe.get_name())
        print "end"
    return usable_recipes

def check_inventory_for_type(typ):

    b_list = db_bottletypes_checkfortype(typ)
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

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    return db_inventory_getamount(mfg,liquor)