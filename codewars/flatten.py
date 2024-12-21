"""
Flatten
https://www.codewars.com/kata/flatten

For this exercise you will create a global flatten method. The method takes in any number of arguments and flattens them into a single array. If any of the arguments passed in are an array then the individual objects within the array will be flattened so that they exist at the same level as the other arguments. Any nested arrays, no matter how deep, should be flattened into the single array result.

Examples:
flatten(1, [2, 3], 4, 5, [6, [7]]) # returns [1, 2, 3, 4, 5, 6, 7]
flatten('a', ['b', 2], 3, None, [[4], ['c']]) # returns ['a', 'b', 2, 3, None, 4, 'c']
"""

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.test_framework import run_tests

def flatten(*args):
    # Solution 1: Using recursive function
    # result = []
    # for arg in args:
    #     if isinstance(arg, list):
    #         result.extend(flatten(*arg))
    #     else:
    #         result.append(arg)
                
    # return result
    
    # Solution 2 using iteration:
    result = []
    stack = list(args)  # Start with the arguments as a list

    while stack:
        current = stack.pop(0)  # Take the first item from the stack
        if isinstance(current, list):
            # If the current item is a list, push all its elements to the stack
            stack = current + stack
        else:
            # Otherwise, append the current item to the result list
            result.append(current)
    
    return result
            
            





def test_solution():
    test_cases = [
        (flatten, [[], []], [], "flatten() should return []"),
        (flatten, [[1, 2, 3]], [1, 2, 3], "flatten(1, 2, 3) should return [1, 2, 3]"),
        (flatten, [[1, 2], [3, 4, 5], [6, [7], [[8]]]], [1, 2, 3, 4, 5, 6, 7, 8], "flatten([1, 2], [3, 4, 5], [6, [7], [[8]]]) should return [1, 2, 3, 4, 5, 6, 7, 8]"),
        (flatten, [[1, 2, ['9', [], []], None]], [1, 2, '9', None], "flatten(1, 2, ['9', [], []], None) should return [1, 2, '9', None]"),
        (flatten, [[['hello', 2, ['text', [4, 5]]], [[]], '[list]']], ['hello', 2, 'text', 4, 5, '[list]'], "flatten(['hello', 2, ['text', [4, 5]]], [[]], '[list]') should return ['hello', 2, 'text', 4, 5, '[list]']"),
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution()