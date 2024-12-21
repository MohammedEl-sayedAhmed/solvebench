"""
20. Valid Parentheses
https://leetcode.com/problems/valid-parentheses/

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.
- Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false

Example 4:
Input: s = "([])"
Output: true

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.
"""

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from common.test_framework import run_tests

class Solution:
    def isValid(self, s: str) -> bool:
        """
        Check if the input string of parentheses is valid.
        
        This solution uses a stack to ensure that every opening bracket has a corresponding closing bracket
        in the correct order.
        
        Time Complexity: O(n)
        Space Complexity: O(n) in the worst case for the stack.
        """
        stack = []
        mapping = {')':'(',
                   '}':'{',
                   ']':'['}
        
        
        for char in s:
            if char in mapping: # this is a closing tag
                if len(stack) != 0:
                    top_element = stack.pop()
                else:
                    top_element = '#'
                if mapping[char] != top_element:
                    return False
            else: # this is opening tag
                stack.append(char)
                
        if len(stack) == 0:
            return True
        else:
            return False
        
            


def test_solution():
   solution = Solution()
   
   test_cases = [
       (solution.isValid, ["()"], True, "Example 1"),
       (solution.isValid, ["()[]{}"], True, "Example 2"),
       (solution.isValid, ["(]"], False, "Example 3"),
       (solution.isValid, ["([])"], True, "Example 4"),
       (solution.isValid, ["()))"], False, "Example 5"),
       (solution.isValid, ["{[()]}"], True, "Nested brackets"),
       (solution.isValid, ["{[(])}"], False, "Incorrect order"),
       (solution.isValid, [""], True, "Empty string"),
       (solution.isValid, ["((((()))))"], True, "Deep nesting"),
       (solution.isValid, ["]"], False, "Single closing bracket"),
       (solution.isValid, ["[({})]"], True, "Mixed brackets")
   ]
   
   run_tests(test_cases)
if __name__ == "__main__":
   test_solution()