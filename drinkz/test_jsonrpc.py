"""
Test the JSON application
"""

from StringIO import StringIO
import simplejson
import urllib

import sys
import os

import db
import recipes
import app


liquor_types = []

def initDB():
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

def make_rpc_call(fn_name, params):
    d = dict(method=fn_name, params=params, id="0")
    encoded = simplejson.dumps(d)
    
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = 'POST'
    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = len(encoded)

    d = {}
    def my_start_response(s, h):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    response = app_obj(environ, my_start_response)

    x = "".join(response)
    response = simplejson.loads(x)
    
    return response['result']

def test_simpleapp_add():
    initDB()
    
    x = make_rpc_call('add', [1,2])
        
    assert x == 3, x

def test_simpleapp_convert_units_to_ml():
    initDB()
    
    x = make_rpc_call('convert_units_to_ml', ['500 gallon'])

    assert '1892705.0' in x

def test_simpleapp_get_recipe_names():
    initDB()

    x = make_rpc_call('get_recipe_names', [])

    assert 'scotch on the rocks' in x
    assert 'whiskey bath' in x

def test_simpleapp_get_liquor_inventory():
    initDB()

    newApp = app.SimpleApp()

    x = make_rpc_call('get_liquor_inventory', [])
    
    print x

    assert ["Gray Goose", "vodka"] in x
    assert ["Uncle Herman's", "moonshine"] in x
    assert ["Johnnie Walker", "black label"] in x
    assert ["Rossi", "extra dry vermouth"] in x
    
def test_simpleapp_inventory_add():
    initDB()

    x = make_rpc_call('inventory_add', ['Johnnie Walker,black label,500 ml'])

    assert db.check_inventory('Johnnie Walker', 'black label') == True
    
def test_simpleapp_bottle_add():
    initDB()

    x = make_rpc_call('bottle_add', ['Johnnie Winner,Blob Zinger,Excellent Milk'])
    
    assert ('Johnnie Winner','Blob Zinger') in db.get_all_bottle_types()   
def test_simpleapp_recipe_add():
   initDB()

   x = make_rpc_call( 'recipe_add', ["Moo Moo Milk Vodka,Mohawk::50 gallon,Milk::3 liter"] )
   names = []
   recipes = db.get_all_recipes()
   for name in recipes:
       names.append(name.get_name())

   assert 'Moo Moo Milk Vodka' in names