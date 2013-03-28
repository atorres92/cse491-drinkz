#! /usr/bin/env python

import os
import drinkz.db
import drinkz.recipes

try:
    os.mkdir('html')
except OSError:
    #already exists
    pass

drinkz.db.load_db('bin/database')

liquor_types = []

for mfg, liquor in drinkz.db.get_liquor_inventory():
    liquor_types.append((mfg, liquor))

###

fp = open('html/index.html', 'w')
print >>fp,"""
<p>Index</p>
<p><a href='recipes.html'>Recipes</a></p>
<p><a href='inventory.html'>Inventory</a></p>
<p><a href='liquor_types.html'>Liquor Types</a></p>"""

fp.close()

###

fp = open('html/recipes.html', 'w')
print >>fp, """
<p><a href='index.html'>Index</a></p>
<p>Recipes</p>
<p><a href='inventory.html'>Inventory</a></p>
<p><a href='liquor_types.html'>Liquor Types</a></p>
<p>Recipes: </p>
<table>
<tr>
  <td> <b>Recipe Name</b> </td>
  <td> <b>Have Ingredients?</b></td>
</tr>"""

for recipe in drinkz.db.get_all_recipes():
    print >>fp, "<tr><td>" + recipe.get_name() + "</td><td>"
    if len(recipe.need_ingredients()) > 0:
        print >>fp, "<td>No :(</td></tr>"
    else:
        print >>fp, "<td>Yup :D </td></tr>"

    
print >>fp,"""
    </tr>
    </table>"""

fp.close()

###

fp = open('html/inventory.html', 'w')
print >>fp, """
<p><a href='index.html'>Index</a></p>
<p><a href='recipes.html'>Recipes</a></p>
<p>Inventory</p>
<p><a href='liquor_types.html'>Liquor Types</a></p>
<p>Inventory:</p>
<table>
  <tr>
    <td><b>Manufacturer</b></td>
    <td><b>Liquor</b></td>
    <td><b>Amount</b></td>
"""
for liquor_typ in liquor_types:
    print >>fp, "<tr><td>" + liquor_typ[0] + "</td><td>" + liquor_typ[1] + "</td><td>" + str(drinkz.db.get_liquor_amount(liquor_typ[0], liquor_typ[1])) + " ml</td></tr>"


print >>fp,"""
  </tr>
</table>
"""

fp.close()

###

fp = open('html/liquor_types.html', 'w')

print >>fp,"""
<p><a href='index.html'>Index</a></p>
<p><a href='recipes.html'>Recipes</a></p>
<p><a href='inventory.html'>Inventory</a></p>
<p>Liquor Types</p>
<p>Liquor Types: </p>
<table>
  <tr>
    <td><b>Manufacturer</b></td>
    <td><b>Liquor</b></td>
  </tr>"""

for liquor_typ in liquor_types:
    print >>fp,"<tr><td>" + liquor_typ[0] + "</td><td>" + liquor_typ[1] + "</td></tr>" 

print >>fp,"""
</table>
"""

fp.close()

###
