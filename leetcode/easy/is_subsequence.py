"""
392. Is Subsequence
https://leetcode.com/problems/is-subsequence/

Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some 
(can be none) of the characters without disturbing the relative positions of the remaining characters. 
(i.e., "ace" is a subsequence of "abcde" while "aec" is not).

Example 1:
Input: s = "abc", t = "ahbgdc"
Output: true

Example 2:
Input: s = "axc", t = "ahbgdc"
Output: false

Constraints:
- 0 <= s.length <= 100
- 0 <= t.length <= 10^4
- s and t consist only of lowercase English letters.

Follow up: Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 10^9, 
and you want to check one by one to see if t has its subsequence. In this scenario, 
how would you change your code?
"""

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from common.test_framework import run_tests

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if len(s) == 0: return True
        if len(t) == 0: return False
        

        s_ptr = 0
        
        for t_char in t:
            if s_ptr < len(s) and s[s_ptr] == t_char:
                s_ptr += 1
                
                if s_ptr == len(s):
                    return True
        
        return False
            
        

def test_solution():
    solution = Solution()
    
    test_cases = [
        (solution.isSubsequence, ["abc", "ahbgdc"], True, "Example 1"),
        (solution.isSubsequence, ["axc", "ahbgdc"], False, "Example 2"),
        (solution.isSubsequence, ["", "ahbgdc"], True, "Empty source string"),
        (solution.isSubsequence, ["abc", ""], False, "Empty target string"),
        (solution.isSubsequence, ["abc", "abc"], True, "Exact match"),
        (solution.isSubsequence, ["abc", "abcde"], True, "Subsequence at start"),
        (solution.isSubsequence, ["abc", "deabc"], True, "Subsequence at end"),
        (solution.isSubsequence, ["abc", "ac"], False, "Target shorter than source"),
        (solution.isSubsequence, ["abcde", "ace"], False, "Source longer than target"),
        (solution.isSubsequence, ["", ""], True, "Both empty strings")
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution() 