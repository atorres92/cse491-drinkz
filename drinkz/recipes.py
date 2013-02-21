# import drinkz.recipes.py

from . import db

class Recipe(object):
    def __init__(self, recipeName, listOfIngredTuples):
        self._name = recipeName
        self._ingredients = listOfIngredTuples #of the form: [('mfg', 'amt ml'),('mfg2', 'amt oz'), ...] 

    def need_ingredients(self):
        neededIng = []
        for ingredient in self._ingredients:
            needed = db.check_recipe_needs(ingredient)
            if needed[1] > 0:
                neededIng.append(needed)
        return neededIng

    def get_name(self):
        return self._name

    def get_ingredients(self):
        return self._ingredients
