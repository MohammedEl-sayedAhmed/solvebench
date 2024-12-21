"""
Pete, the Baker
https://www.codewars.com/kata/pete-the-baker

Pete likes to bake some cakes. He has some recipes and ingredients. Unfortunately he is not good in maths. Can you help him to find out, how many cakes he could bake considering his recipes?

Write a function cakes(), which takes the recipe (object) and the available ingredients (also an object) and returns the maximum number of cakes Pete can bake (integer). For simplicity there are no units for the amounts (e.g. 1 lb of flour or 200 g of sugar are simply 1 or 200). Ingredients that are not present in the objects, can be considered as 0.

Examples:
# must return 2
cakes({'flour': 500, 'sugar': 200, 'eggs': 1}, {'flour': 1200, 'sugar': 1200, 'eggs': 5, 'milk': 200})
# must return 0
cakes({'apples': 3, 'flour': 300, 'sugar': 150, 'milk': 100, 'oil': 100}, {'sugar': 500, 'flour': 2000, 'milk': 2000})
"""

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.test_framework import run_tests

def cakes(recipe, available):
    maxCake = float('inf')
    for ingredient, amount in recipe.items():
        if ingredient not in available:
            return 0
        canDo = available[ingredient] // amount
        if canDo < maxCake:
            maxCake = canDo
    # print(maxCake)   
    return maxCake 

def test_solution():
    test_cases = [
        (cakes, [{"flour": 500, "sugar": 200, "eggs": 1}, {"flour": 1200, "sugar": 1200, "eggs": 5, "milk": 200}], 2, "Test Case 1"),
        (cakes, [{"apples": 3, "flour": 300, "sugar": 150, "milk": 100, "oil": 100}, {"sugar": 500, "flour": 2000, "milk": 2000}], 0, "Test Case 2"),
        (cakes, [{"flour": 100, "sugar": 100}, {"flour": 300, "sugar": 300, "eggs": 5}], 3, "Test Case 3"),
        (cakes, [{"flour": 1, "sugar": 1}, {"flour": 1, "sugar": 1}], 1, "Test Case 4"),
        (cakes, [{"flour": 1}, {"sugar": 1}], 0, "Test Case 5"),
        (cakes, [{"apples": 3, "flour": 300, "sugar": 150, "milk": 100, "oil": 100}, {"sugar": 500, "flour": 2000, "milk": 2000, "apples": 15, "oil": 20}], 0, "Test Case 6"),
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution() 