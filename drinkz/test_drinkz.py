"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and exxecuted (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data, recipes

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    
def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_inventory_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    data = "           ,            ,               "
    fp = StringIO(data)
    n = load_bulk_data.load_inventory(fp)
    
    assert n == 0, n
    
def test_bulk_load_inventory_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    data = "#Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)
    n = load_bulk_data.load_inventory(fp)

    assert n == 0, n

    #bulk load recipes
def test_bulk_load_recipes_1():
    db._reset_db()

    data = "scotch on the rocks,blended scotch::4 oz,vodka::20 ml\nblended death,blended milk::10 gallon,hotsauce::20oz,wine::2 ml"
    fp = StringIO(data)
    n = load_bulk_data.load_recipes(fp)

    assert n == 2, n

def test_bulk_load_recipes_2():
    db._reset_db()

    data = "scotch with spoiled milks,blended vodka::5 liter,orange juice::2 oz,green tea::200ml,white sambooka::20 gallon,blended mystery meat::1 ml"
    fp = StringIO(data)
    n = load_bulk_data.load_recipes(fp)

    assert n == 1, n

def test_bulk_load_recipes_3():
    db._reset_db()

    data = "#extra sweet milk\n            ,       ,,,,       ,  "
    fp = StringIO(data)
    n = load_bulk_data.load_recipes(fp)

    assert n == 0, n
    
def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount

def test_get_liquor_amount_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml\nJohnnie Walker,Black Label,28 oz"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1828.058, amount
    
def test_get_liquor_amount_4():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml\nJohnnie Walker,Black Label,28 oz\nJohnnie Weener,Delicious Label, 9830ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1828.058, amount

def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_bottle_types_2():
    db._reset_db()

    data = "     ,     ,    "
    fp = StringIO(data)
    n = load_bulk_data.load_bottle_types(fp)

    assert n == 0, n
    
def test_bulk_load_bottle_types_3():
    db._reset_db()

    data = "#Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)
    n = load_bulk_data.load_bottle_types(fp)

    assert n == 0, n

def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_bottle_types_2():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-2.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_bottle_types_3():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-3.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_inventory_1():
    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/inventory-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_inventory_2():
    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/inventory-data-2.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_inventory_3():
    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/inventory-data-3.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x

def test_get_bottle_types():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Milk Label', 'blended milk')
    db.add_bottle_type('Johnnie Weens', 'Milky Labels', 'okayface.jpg')

    numBottleTypes = len(db.get_all_bottle_types())

    assert numBottleTypes == 2, numBottleTypes
    
def test_get_usable_recipes():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    r1 = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
    r2 = recipes.Recipe('whiskey bath', [('blended scotch', '6 liter')])

    db.add_recipe(r1)
    db.add_recipe(r2)
    
    usableRecipes = db.get_usable_recipes()
    assert usableRecipes == ['scotch on the rocks'], usableRecipes  
    
