"""
Weight for Weight
https://www.codewars.com/kata/weight-for-weight

My friend John and I are members of the "Fat to Fit Club (FFC)". John is worried because each month a list with the weights of members is published and each month he is the last on the list which means he is the heaviest.

I am the one who establishes the list so I told him: "Don't worry any more, I will modify the order of the list". It was decided to attribute a "weight" to numbers. The weight of a number will be from now on the sum of its digits.

For example 99 will have "weight" 18, 100 will have "weight" 1 so in the list 100 will come before 99.

Given a string with the weights of FFC members in normal order can you give this string ordered by "weights" of these numbers?

Example:
Input: "56 65 74 100 99 68 86 180 90"
Output: "100 180 90 56 65 74 68 86 99"

Notes:
- When two numbers have the same "weight", let us class them as if they were strings (alphabetical ordering) and not numbers.
- All numbers in the list are positive numbers and the list can be empty.
- The input string may have leading, trailing whitespaces and more than a unique whitespace between two consecutive numbers.
"""
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.test_framework import run_tests
class Solution:
    def order_weight(self, strng: str) -> str:
        
        weightsList = strng.split()
        
        def getWeight(num: str) -> int:
            numSum = 0
            for digit in num:
                numSum += int(digit)
            return numSum
        
        # for num in weightsList:
        #     weight = getWeight(num)
        #     print(weight)
        
        sortedWeight = [] 
        
        # (getWeight(x),x) ->> Sort the weights first by their digit sum [(getWeight(x)], then by their string representation [x]
        sortedWeight = sorted(weightsList, key= lambda x: (getWeight(x),x))
        sortedWeight= " ".join(sortedWeight)
        
        return sortedWeight
                
        


def test_solution():
    solution = Solution()
    
    test_cases = [
        (solution.order_weight, ["103 123 4444 99 2000"], "2000 103 123 4444 99", "Test Case 1"),
        (solution.order_weight, ["2000 10003 1234000 44444444 9999 11 11 22 123"], "11 11 2000 10003 22 123 1234000 44444444 9999", "Test Case 2"),
        (solution.order_weight, [""], "", "Test Case 3 - Empty input"),
        (solution.order_weight, ["56 65 74 100 99 68 86 180 90"], "100 180 90 56 65 74 68 86 99", "Example 1"),
        (solution.order_weight, ["100 99"], "100 99", "Two numbers with different weights"),
        (solution.order_weight, ["99 100"], "100 99", "Two numbers with different weights"),
        (solution.order_weight, ["56 65 74 68 86 99"], "56 65 74 68 86 99", "No 100 or 180"),
        (solution.order_weight, ["  56  65  74  100  99  "], "100 56 65 74 99", "Leading and trailing spaces"),
        (solution.order_weight, ["56 65 74 100 99 68 86 180 90 90"], "100 180 90 90 56 65 74 68 86 99", "Duplicate numbers"),
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution() 