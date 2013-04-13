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

def test_simpleapp_add():
    initDB()

    newApp = app.SimpleApp()

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    testDict = dict(method='add', params=[1,2], id=1)
    encodedJSON = simplejson.dumps(testDict)

    environ['wsgi.input'] = StringIO(encodedJSON)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s, h, return_in=testDict):
        testDict['status'] = s
        testDict['headers'] = h

    results = newApp.__call__(environ, my_start_response)
    text = "".join(results)

    assert text.find('3') != -1, text

def test_simpleapp_convert_units_to_ml():
    initDB()

    newApp = app.SimpleApp()

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='convert_units_to_ml', params=['500 gallon'], id=1)
    encodedJSON = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encodedJSON)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s,h,return_in=d):
        d['status'] = s
        d['headers'] = h

    results = newApp.__call__(environ, my_start_response)
    text = "".join(results)

    assert text.find('1892705.0') != -1, text

def test_simpleapp_get_recipe_names():
    initDB()

    newApp = app.SimpleApp()

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='get_recipe_names', params=[], id=1)
    encodedJSON = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encodedJSON)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s,h,return_in=d):
        d['status'] = s
        d['headers'] = h

    results = newApp.__call__(environ, my_start_response)
    text = "".join(results)

    assert text.find('scotch on the rocks') != -1, text
    assert text.find('whiskey bath') != -1, text

def test_simpleapp_get_liquor_inventory():
    initDB()

    newApp = app.SimpleApp()

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='get_liquor_inventory', params=[], id=1)
    encodedJSON = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encodedJSON)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s,h,return_id=d):
        d['status'] = s
        d['headers'] = h

    results = newApp.__call__(environ, my_start_response)
    text = "".join(results)

    assert text.find("Gray Goose\", \"vodka") != -1, text
    assert text.find("Uncle Herman's\", \"moonshine") != -1, text
    assert text.find("Johnnie Walker\", \"black label") != -1, text
    assert text.find("Rossi\", \"extra dry vermouth") != -1, text
    
def test_simpleapp_inventory_add():
    initDB()

    newApp = app.SimpleApp()

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    
    d = dict(method='inventory_add', params=['Johnnie Walker,black label,500 ml'], id=1)
    encodedJSON = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encodedJSON)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s,h,return_id=d):
        d['status'] = s
        d['headers'] = h

    results = newApp.__call__(environ, my_start_response)
    text = "".join(results)

    result = db.check_inventory("Johnnie Walker", "black label")

    assert result != False, result
    
def test_simpleapp_bottle_add():
    initDB()

    newApp = app.SimpleApp()

    environ = {}
    environ['REQUEST_METHOD'] = 'POST'
    environ['PATH_INFO'] = '/rpc'

    d = dict(method='bottle_add', params=['Johnnie Winner,Blob Zinger,Excellent Milk'], id=1)
    encodedJSON = simplejson.dumps(d)

    environ['wsgi.input'] = StringIO(encodedJSON)
    environ['CONTENT_LENGTH'] = 1000

    def my_start_response(s,h,return_id=d):
        d['status'] = s
        d['headers'] = h

    results = newApp.__call__(environ, my_start_response)
    text = "".join(results)

    result = ("Johnnie Winner", "Blob Zinger") in db.get_all_bottle_types()

    assert result != False, result
    
def test_simpleapp_recipe_add():
   initDB()

   newApp = app.SimpleApp()

   environ = {}
   environ['REQUEST_METHOD'] = 'POST'
   environ['PATH_INFO'] = '/rpc'

   d = dict(method='recipe_add', params=["Moo Moo Milk Vodka,Mohawk::50 gallon,Milk::3 liter"], id=1)
   encodedJSON = simplejson.dumps(d)

   environ['wsgi.input'] = StringIO(encodedJSON)
   environ['CONTENT_LENGTH'] = 1000

   def my_start_response(s,h,return_id=d):
       d['status'] = s
       d['headers'] = h

   results = newApp.__call__(environ, my_start_response)
   text = "".join(results)

   result = False
   for recipe in db.get_all_recipes():
       if ( recipe.get_name() == "Moo Moo Milk Vodka" ):
           result = True

   assert result != False, result
