"""
125. Valid Palindrome
https://leetcode.com/problems/valid-palindrome/

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters 
and removing all non-alphanumeric characters, it reads the same forward and backward. 
Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Example 3:
Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters.
"""

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from common.test_framework import run_tests


class Solution:
    def isAlphaNum(self,c):
            return_val = False
            if((ord('A') <= ord(c) <= ord('Z')) or
               (ord('a') <= ord(c) <= ord('z')) or
               (ord('0') <= ord(c) <= ord('9'))):
                return_val = True
            return return_val
    def isPalindrome(self, s: str) -> bool:
        
        # Solution 1
        """
        newStr = ""
        for c in s:
            if c.isalnum():
                newStr += c.lower()
        
        #reverse string
        reversedStr = newStr[::-1]
        if newStr == reversedStr:
            return True
        else:
            return False
        """
                
        # Solution 2
        

        
        L = 0
        R = len(s) - 1
        
        while(L < R):
            while((self.isAlphaNum(s[L]) == False) and (L < R)):
                L += 1
            while((self.isAlphaNum(s[R]) == False) and (R > L)):
                R -= 1
                
            if s[L].lower() != s[R].lower():
                return False
            L = L + 1
            R = R - 1
            
        return True

def test_solution():
    solution = Solution()
    
    test_cases = [
        (solution.isPalindrome, ["A man, a plan, a canal: Panama"], True, "Example 1"),
        (solution.isPalindrome, ["race a car"], False, "Example 2"),
        (solution.isPalindrome, [" "], True, "Example 3"),
        (solution.isPalindrome, ["12321"], True, "Numeric palindrome"),
        (solution.isPalindrome, ["0P"], False, "Mixed alphanumeric"),
        (solution.isPalindrome, ["ab_a"], True, "String with underscore"),
        (solution.isPalindrome, [""], True, "Empty string"),
        (solution.isPalindrome, ["!@#$"], True, "Special characters only"),
        (solution.isPalindrome, ["Race a Car"], False, "Case sensitivity test")
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution()
