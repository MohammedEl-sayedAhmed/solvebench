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
    """
    Test function with various test cases to verify the solution.
    """
    solution = Solution()
    
    test_cases = [
        ("()", True, "Example 1"),
        ("()[]{}", True, "Example 2"),
        ("(]", False, "Example 3"),
        ("([])", True, "Example 4"),
        ("()))", False, "Example 5"),
        ("{[()]}", True, "Nested brackets"),
        ("{[(])}", False, "Incorrect order"),
        ("", True, "Empty string"),
        ("((((()))))", True, "Deep nesting"),
        ("]", False, "Single closing bracket"),
        ("[({})]", True, "Mixed brackets")
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for s, expected, test_name in test_cases:
        result = solution.isValid(s)
        if result == expected:
            print(f"✅ {test_name} passed")
            passed_tests += 1
        else:
            print(f"\n❌ {test_name} failed")
            print(f"   Input: s = \"{s}\"")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")
    
    print(f"\nTest Results: {passed_tests}/{total_tests} passed")
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
    else:
        print(f"Failed {total_tests - passed_tests} tests")


if __name__ == "__main__":
    test_solution() 