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
        ("A man, a plan, a canal: Panama", True, "Example 1"),
        ("race a car", False, "Example 2"),
        (" ", True, "Example 3"),
        ("12321", True, "Numeric palindrome"),
        ("0P", False, "Mixed alphanumeric"),
        ("ab_a", True, "String with underscore"),
        ("", True, "Empty string"),
        ("!@#$", True, "Special characters only"),
        ("Race a Car", False, "Case sensitivity test")
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for input_str, expected, test_name in test_cases:
        result = solution.isPalindrome(input_str)
        if result == expected:
            print(f"✅ {test_name} passed")
            passed_tests += 1
        else:
            print(f"\n❌ {test_name} failed")
            print(f"   Input string: \"{input_str}\"")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")
    
    print(f"\nTest Results: {passed_tests}/{total_tests} passed")
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
    else:
        print(f"Failed {total_tests - passed_tests} tests")


if __name__ == "__main__":
    test_solution()
