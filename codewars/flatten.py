"""
Flatten
https://www.codewars.com/kata/flatten

For this exercise you will create a global flatten method. The method takes in any number of arguments and flattens them into a single array. If any of the arguments passed in are an array then the individual objects within the array will be flattened so that they exist at the same level as the other arguments. Any nested arrays, no matter how deep, should be flattened into the single array result.

Examples:
flatten(1, [2, 3], 4, 5, [6, [7]]) # returns [1, 2, 3, 4, 5, 6, 7]
flatten('a', ['b', 2], 3, None, [[4], ['c']]) # returns ['a', 'b', 2, 3, None, 4, 'c']
"""

def flatten(*args):
    result = []
    for arg in args:
        if isinstance(arg, list):
            result.extend(flatten(*arg))
        else:
            result.append(arg)
                
    return result





def test_solution():
    """
    Test function with various test cases to verify the solution.
    """
    test_cases = [
        ([], []),  # flatten() should return []
        ([1, 2, 3], [1, 2, 3]),  # flatten(1, 2, 3) should return [1, 2, 3]
        ([1, 2], [3, 4, 5], [6, [7], [[8]]], [1, 2, 3, 4, 5, 6, 7, 8]),  # flatten([1, 2], [3, 4, 5], [6, [7], [[8]]]) should return [1, 2, 3, 4, 5, 6, 7, 8]
        ([1, 2, ['9', [], []], None], [1, 2, '9', None]),  # flatten(1, 2, ['9', [], []], None) should return [1, 2, '9', None]
        ([['hello', 2, ['text', [4, 5]]], [[]], '[list]'], ['hello', 2, 'text', 4, 5, '[list]']),  # flatten(['hello', 2, ['text', [4, 5]]], [[]], '[list]') should return ['hello', 2, 'text', 4, 5, '[list]']
    ]
    
    for case in test_cases:
        args, expected = case[:-1], case[-1]  # Separate the last element as expected output
        result = flatten(*args)
        if result == expected:
            print(f"✅ Test Case passed")
        else:
            print(f"❌ Test Case failed")
            print(f"   Input: {args}")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")

if __name__ == "__main__":
    test_solution()