#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import db
import load_bulk_data
import recipes
import convert
import jinja2

import sys

from cStringIO import StringIO
import imp

dispatch = {
    '/' : 'index',
    '/error' : 'error',
    '/recv' : 'recv',
    '/recv_inventory_add' : 'recv_inventory_add',
    '/recv_bottle_add' : 'recv_bottle_add',
    '/recv_recipe_add' : 'recv_recipe_add',
    '/rpc'  : 'dispatch_rpc',
    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/liquortypes' : 'liquortypes',
    '/converter' : 'converter'
}

bodyText = """
<p><a href='./'>Index</a></p>
<p><a href='recipes'>Recipes</a></p>
<p><a href='inventory'>Inventory</a></p>
<p><a href='liquortypes'>Liquor Types</a></p>
<p><a href='converter'>Converter</a></p>
"""

html_headers = [('Content-type', 'text/html')]
#liquor_types = []

def initDB():
    db.load_db('database')

#    for mfg, liquor in db.get_liquor_inventory():
#        liquor_types.append((mfg, liquor))

    # Run-web should do configuration file
    #Specifiy file for run-web in init_
class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = """
<html>
<title>cse491-drinkz home</title>
<head>
<style type="text/css">
h1 {color:red;}</style><b><h1>Home Page</h1></b></head>
<body>
<p>Index</p>
<p><a href='recipes'>Recipes</a></p>
<p><a href='inventory'>Inventory</a></p>
<p><a href='liquortypes'>Liquor Types</a></p>
<p><a href='converter'>Converter</a></p>
</body>
<script>
function alertBox()
{
alert("What were you thinking?!");
}
</script>
<input type="button" onclick="alertBox()" value="DON'T CLICK!">
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]

    def recipes(self, environ, start_response):
        content_type = 'text/html'
        data = recipes()

        start_response('200 OK', list(html_headers))
        return[data]

    def inventory(self, environ, start_response):
        content_type = 'text/html'
        data = inventory()
        start_response('200 OK', list(html_headers))
        return[data]
    
    def liquortypes(self, environ, start_response):
        content_type = 'text/html'
        data = liquortypes()
        start_response('200 OK', list(html_headers))
        return[data]
    
    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def converter(self, environ, start_response):
        data = converter()
        
        start_response('200 OK', list(html_headers))
        return [data]

    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        if ( 'amount' in results.keys() ):
            amount = results['amount'][0]
        else:
            amount = '0 ml'

        amount = str(convert.convert_to_ml(amount))
        
        content_type = 'text/html'
        data = "Converted Amount: %s ml<p><a href='./'>Index</a>" % amount

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_inventory_add(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        if ( 'liquor' in results.keys() ):
            liquorStr = results['liquor'][0]
        else:
            liquorStr = "#"

        content_type = 'text/html'

        data = liquorStr
        fp = StringIO(data)
        load_bulk_data.load_inventory(fp)
        data = "Added Liquor: %s<p><a href='./'>Index</a>" % liquorStr

        start_response('200 OK', list(html_headers) )
        return [data]

    def recv_bottle_add(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        if ( 'bottle' in results.keys() ):
            bottleStr = results['bottle'][0]
        else:
            bottleStr = "#"

        content_type = 'text/html'

        data = bottleStr
        fp = StringIO(data)
        load_bulk_data.load_bottle_types(fp)
        #db.get_all_bottle_types()
        data = "Added Bottle Type: %s<p><a href='./'>Index</a>" % bottleStr

        start_response('200 OK', list(html_headers) )
        return [data]
    
    def recv_recipe_add(self, environ, start_response):
        
        print "hi"
        
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        if ( 'recipe' in results.keys() ):
            recipeStr = results['recipe'][0]
        else:
            recipeStr = '#'

        data = recipeStr
        fp = StringIO(data)
        load_bulk_data.load_recipes(fp)

        content_type = 'text/html'
        data = "Added Recipe: %s<p><a href='./'>Index</a>" % recipeStr
        
        start_response('200 OK', list(html_headers) )
        return [data]
    
    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)
    
    def rpc_convert_units_to_ml( self, amount ):
        return str( convert.convert_to_ml(amount) )

    def rpc_get_recipe_names( self ):
        r = db.get_all_recipes()
        final = []
        for recipe in r:
            final.append(recipe.get_name())
        return final

    def rpc_get_liquor_inventory( self ):
        i = list()
        for (m,l) in db.get_liquor_inventory():
            i.append((m,l))
        return i

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)

    def rpc_inventory_add( self, item ):
        data = item
        fp = StringIO(data)
        load_bulk_data.load_inventory(fp)
        
    def rpc_bottle_add( self, bottle ):
        data = bottle
        fp = StringIO(data)
        load_bulk_data.load_bottle_types(fp)
        
    def rpc_recipe_add( self, recipe ):
        data = recipe
        fp = StringIO(data)
        load_bulk_data.load_recipes(fp)
    
def converter():
    loader = jinja2.FileSystemLoader('../drinkz/templates')

    env = jinja2.Environment(loader=loader)

    filename = "jinja_converter.html"

    vars = dict(title = "Convert to mL", title2="Enter conversion", form = """
<form action='recv'>
Amount of liquid to convert to ml? <input type='text' name='amount' size'20'>
<input type='submit'>
</form>
""", names = "")

    result = env.get_template(filename).render(vars).encode('ascii','ignore')
    return result

def recipes():

    #this sets up jinja2
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    #pick filename to render
    filename = "jinja_recipes.html"

    recipeList = []
    for recipe in db.get_all_recipes():
        if len(recipe.need_ingredients()) > 0:
            result = "No :("
        else:
            result = "Yup :D"

        recipeList.append(list([recipe.get_name(), result]))

    vars = dict(title = 'Recipes Here!', title2 = 'Recipes', addtitle = "Submit Recipe",
                form = """ <form action='recv_recipe_add'>
Recipe to add? (Format: recipeName,ingrName::ingrAmt ml,ingrName2::ingrAmt2 gallon)<br><input type='text' name='recipe' size'20'>
<input type='submit'>
</form> """, names = recipeList, bodyFormat = bodyText)

    #Since Nosetests will fail since it isn't run in the drinkz directory, but in the home dir :( 
    try:
        template = env.get_template(filename)
    except:
        loader = jinja2.FileSystemLoader('./drinkz/templates')
        env = jinja2.Environment(loader=loader)
        template = env.get_template(filename)
        
    result = template.render(vars).encode('ascii','ignore')
    return result
    
def inventory():

    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    filename = "jinja_inventory.html"

    inventoryList = []
    for liquor_typ in db.get_all_bottle_types():
        inventoryList.append(list([str(liquor_typ[0]), str(liquor_typ[1]), str(db.get_liquor_amount(liquor_typ[0], liquor_typ[1])) + " ml"]))

    vars = dict(title = "Inventory", title2 = "Your Inventory", addtitle = "Add To Your Inventory", form = """
<form action='recv_inventory_add'>
Liquor to add? (Format: Johnnie Walker, black label, 500 ml)<br><input type='text' name='liquor' size'20'>
<input type='submit'>
</form>
""", names=inventoryList, bodyFormat = bodyText)

    template = env.get_template(filename)

    result = template.render(vars).encode('ascii','ignore')
    return result
                
def liquortypes():
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)

    filename = "jinja_bottle_types.html"

    liquortypesList = []
    
    for liquor_typ in db.get_all_bottle_types():
        liquortypesList.append(list([str(liquor_typ[0]), str(liquor_typ[1])]))

    vars = dict(title = "Liquor Types", title2 = "Your Liquor Types", addtitle="Add Bottle Type", form = """
<form action='recv_bottle_add'>
Bottle Type to add? (Format: Johnnie Walker, black label, blended scotch whiskey)<br><input type='text' name='bottle' size'20'>
<input type='submit'>
</form>
</body></html>""", names=liquortypesList, bodyFormat = bodyText)

    template = env.get_template(filename)

    result = template.render(vars).encode('ascii','ignore')
    
    return result


def startServer():
    import random, socket
    port = random.randint(8000, 9999)

    initDB()
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
        (socket.getfqdn(), port)
    httpd.serve_forever()

