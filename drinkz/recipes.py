# import drinkz.recipes.py

import db

class Recipe(object):
    def __init__(self, recipeName, listOfIngredTuples):
        self._name = recipeName
        self._ingredients = listOfIngredTuples #of the form: [('mfg', 'amt ml'),('mfg2', 'amt oz'), ...] 

    def need_ingredients(self):
        neededIng = []
        for ingredient in _ingredients:
            needed = db._check_recipe_needs(ingredient)
            if needed[1] > 0:
                neededIng.append(ingredient)
        return neededIng
