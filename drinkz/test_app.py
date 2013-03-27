import sys
import os

import db
import recipes
import app
import urllib

def dbInit():    
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


def test_generated_page():

    dbInit()

    testApp = app.SimpleApp()

    environ = {}
    environ['QUERY_STRING'] = urllib.urlencode(dict(firstname='FOO', lastname='BOB'))

    environ['PATH_INFO'] = '/recipes'

    myDict = {}

    def my_start_response(s, h, return_in=myDict):
        myDict['status'] = s
        myDict['headers'] = h

    results = testApp.__call__(environ, my_start_response)

    testText = "".join(results)

    assert testText.find("scotch on the rocks") != 1, testText
    assert testText.find("whiskey bath") != 1, testText

