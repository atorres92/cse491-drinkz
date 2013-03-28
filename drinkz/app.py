#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import db
import recipes
import convert

import sys

dispatch = {
    '/' : 'index',
    '/error' : 'error',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc',
    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/liquortypes' : 'liquortypes',
    '/converter' : 'converter'
}

html_headers = [('Content-type', 'text/html')]
liquor_types = []

def initDB():
    db.load_db('database')

    for mfg, liquor in db.get_liquor_inventory():
        liquor_types.append((mfg, liquor))

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
        return db.get_all_recipes()

    def rpc_get_liquor_inventory( self ):
        return get_liquor_inventory()

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)
    
def converter():
    return """
<html>
<title>Convert to mL</title>
<head><style type="text/css">
h1 {color:red;}</style><b><h1>Converter</h1></b></head>
<body>
<form action='recv'>
Amount of liquid to convert to ml? <input type='text' name='amount' size'20'>
<input type='submit'>
</form>
<p><a href='./'>Index</a></p>
</body>
</html>
"""
        
def recipes():
    html =  """
<html>
<title>Recipes here!</title>
<head><style type="text/css">
h1 {color:red;}</style><b><h1>Recipes</h1></b></head>
<body>
<p><a href='./'>Index</a></p>
<p>Recipes</p>
<p><a href='inventory'>Inventory</a></p>
<p><a href='liquortypes'>Liquor Types</a></p>
<p><a href='converter'>Converter</a></p>
<p>Recipes: </p>
<table>
<tr>
  <td> <b>Recipe Name</b> </td>
    <td> <b>Have Ingredients?</b></td>
    </tr>"""
    result =""
    name = ""
    final = ""
    for recipe in db.get_all_recipes():
        name =  "<tr><td>" + recipe.get_name() + "</td><td>"
        if len(recipe.need_ingredients()) > 0:
            result =  "<td>No :(</td></tr>"
        else:
            result =  "<td>Yup :D </td></tr>"
        final += name + result


    end = """</tr></table></body></html>"""
    return html + final + end

def inventory():
    html =  """
<html>
<title>Inventory!!!</title>
<head><style type="text/css">
h1 {color:red;}</style><b><h1>Your inventory</h1></b></head>
<body>
<p><a href='./'>Index</a></p>
<p><a href='recipes'>Recipes</a></p>
<p>Inventory</p>
<p><a href='liquortypes'>Liquor Types</a></p>
<p><a href='converter'>Converter</a></p>
<p>Inventory:</p>
<table>
  <tr>
      <td><b>Manufacturer</b></td>
          <td><b>Liquor</b></td>
              <td><b>Amount</b></td>
              """
    result = ""
    for liquor_typ in liquor_types:
        result += "<tr><td>" + liquor_typ[0] + "</td><td>" + liquor_typ[1] + "</td><td>" + str(db.get_liquor_amount(liquor_typ[0], liquor_typ[1])) + " ml</td></tr>"

    end = """</tr></table></body></html>"""
    return html + result + end

def liquortypes():
    html = ""
    temp = ""
    final = ""
    end = ""
    
    html = """
<html><title>Liquor types!</title><head><style type="text/css">
h1 {color:red;}</style><b><h1>Liquor Types</h1></b></head>
    <body><p><a href='./'>Index</a></p>
    <p><a href='recipes'>Recipes</a></p>
    <p><a href='inventory'>Inventory</a></p>
    <p>Liquor Types</p>
    <p><a href='converter'>Converter</a></p>
    <p>Liquor Types: </p>
    <table>
    <tr>
      <td><b>Manufacturer</b></td>
          <td><b>Liquor</b></td>
            </tr>"""
    for liquor_typ in liquor_types:
        temp = "<tr><td>" + liquor_typ[0] + "</td><td>" + liquor_typ[1] + "</td></tr>"
        final += temp
    end = """</table></body></html>"""
    return html + final + end


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
