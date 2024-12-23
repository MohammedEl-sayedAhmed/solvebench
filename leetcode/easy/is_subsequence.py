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


# Solution 1: Brute Force Approach (Naive Solution)
class BruteForceSolution:
    def isSubsequence(self, s: str, t: str) -> bool:
        """
        Brute Force Approach:
        - This solution generates all possible subsequences of `t` and checks if `s` is one of them.
        - It uses a helper function to generate subsequences of `t` and checks for membership of `s` in those subsequences.
        - The approach is very inefficient for larger inputs, as it has exponential time complexity due to generating all subsequences.
        
        Time Complexity: O(2^m), where `m` is the length of `t`. This is because generating all subsequences of `t`
        requires iterating over all subsets of `t`, which grows exponentially.
        """
        def generate_subsequences(t: str):
            subsequences = ['']
            for char in t:
                subsequences += [subseq + char for subseq in subsequences]
            return subsequences

        return s in generate_subsequences(t)


# Solution 2: Two-Pointer Approach (Optimal Solution)
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        """
        Two-Pointer Approach:
        - This solution uses two pointers: one for `s` and one for `t`.
        - We iterate through `t`, and whenever we find a character in `t` that matches the current character in `s`, 
          we move the pointer on `s`. If we match all characters of `s` before reaching the end of `t`, then `s` is a subsequence of `t`.
        
        - This approach is very efficient because we make a single pass through `t` and only check each character of `s` once.
        
        Time Complexity: O(n), where `n` is the length of `t`. This is because we make a single pass through `t` and perform constant-time comparisons.
        """
        if len(s) == 0: return True  # If s is empty, it is trivially a subsequence of t
        if len(t) == 0: return False  # If t is empty but s is not, it can't be a subsequence

        s_ptr = 0  # Pointer for string s
        
        # Iterate through t and try to match characters with s
        for t_char in t:
            if s_ptr < len(s) and s[s_ptr] == t_char:
                s_ptr += 1  # Move pointer on s when we find a match
                if s_ptr == len(s):  # If we've matched all characters of s
                    return True
        
        return False  # If we finished the loop without matching all characters of s


# Solution 3: Preprocessing with Index Map + Binary Search (Optimized Solution)
class OptimizedSolution:
    def isSubsequence(self, s: str, t: str) -> bool:
        """
        Optimized Solution using Preprocessing with Index Map and Binary Search:
        - In this solution, we first preprocess `t` by storing the indices of each character in a dictionary.
        - For each character in `s`, we perform a binary search to find the next occurrence of that character in `t` that comes after the current position.
        - The preprocessing step allows for faster lookup, and binary search ensures we can efficiently find the next valid index.
        
        - This approach is especially useful when we need to perform multiple queries on the same `t`, as the preprocessing step only needs to be done once.
        
        Time Complexity:
        - Preprocessing: O(m), where `m` is the length of `t`. We iterate through `t` and build an index map.
        - Querying: O(k log m), where `k` is the length of `s` and `m` is the length of `t`. For each character of `s`, we perform a binary search on the list of indices in the index map.
        - Overall Time Complexity: O(m + k log m) for a single query.
        """
        if len(s) == 0: return True  # If s is empty, it's trivially a subsequence
        if len(t) == 0: return False  # If t is empty but s is not, it can't be a subsequence
        
        from bisect import bisect_left
        
        # Preprocess t to create a map of character positions
        char_positions = {}
        for i, char in enumerate(t):
            if char not in char_positions:
                char_positions[char] = []
            char_positions[char].append(i)
        
        current_pos = -1  # Starting before the first character of t
        
        # Now, check if we can find each character of s in the remaining part of t
        for char in s:
            if char not in char_positions:
                return False  # If the character is not in t at all
            
            # Binary search to find the smallest index > current_pos
            positions = char_positions[char]
            idx = bisect_left(positions, current_pos + 1)
            if idx == len(positions):
                return False  # No valid position found
            
            current_pos = positions[idx]  # Move to the next valid position
        
        return True


def test_solution():
    solution = Solution()
    optimized_solution = OptimizedSolution()
    brute_force_solution = BruteForceSolution()
    
    test_cases = [
        # Test the brute force solution
        (brute_force_solution.isSubsequence, ["abc", "ahbgdc"], True, "Example 1 (Brute Force)"),
        (brute_force_solution.isSubsequence, ["axc", "ahbgdc"], False, "Example 2 (Brute Force)"),
        (brute_force_solution.isSubsequence, ["", "ahbgdc"], True, "Empty source string (Brute Force)"),
        (brute_force_solution.isSubsequence, ["abc", ""], False, "Empty target string (Brute Force)"),
        (brute_force_solution.isSubsequence, ["abc", "abc"], True, "Exact match (Brute Force)"),
        (brute_force_solution.isSubsequence, ["abc", "abcde"], True, "Subsequence at start (Brute Force)"),
        (brute_force_solution.isSubsequence, ["abc", "deabc"], True, "Subsequence at end (Brute Force)"),
        (brute_force_solution.isSubsequence, ["abc", "ac"], False, "Target shorter than source (Brute Force)"),
        (brute_force_solution.isSubsequence, ["abcde", "ace"], False, "Source longer than target (Brute Force)"),
        (brute_force_solution.isSubsequence, ["", ""], True, "Both empty strings (Brute Force)"),

        # Test the two-pointer solution
        (solution.isSubsequence, ["abc", "ahbgdc"], True, "Example 1 (Two-Pointer)"),
        (solution.isSubsequence, ["axc", "ahbgdc"], False, "Example 2 (Two-Pointer)"),
        (solution.isSubsequence, ["", "ahbgdc"], True, "Empty source string (Two-Pointer)"),
        (solution.isSubsequence, ["abc", ""], False, "Empty target string (Two-Pointer)"),
        (solution.isSubsequence, ["abc", "abc"], True, "Exact match (Two-Pointer)"),
        (solution.isSubsequence, ["abc", "abcde"], True, "Subsequence at start (Two-Pointer)"),
        (solution.isSubsequence, ["abc", "deabc"], True, "Subsequence at end (Two-Pointer)"),
        (solution.isSubsequence, ["abc", "ac"], False, "Target shorter than source (Two-Pointer)"),
        (solution.isSubsequence, ["abcde", "ace"], False, "Source longer than target (Two-Pointer)"),
        (solution.isSubsequence, ["", ""], True, "Both empty strings (Two-Pointer)"),

        # Test the optimized solution with index map and binary search
        (optimized_solution.isSubsequence, ["abc", "ahbgdc"], True, "Example 1 (Optimized)"),
        (optimized_solution.isSubsequence, ["axc", "ahbgdc"], False, "Example 2 (Optimized)"),
        (optimized_solution.isSubsequence, ["", "ahbgdc"], True, "Empty source string (Optimized)"),
        (optimized_solution.isSubsequence, ["abc", ""], False, "Empty target string (Optimized)"),
        (optimized_solution.isSubsequence, ["abc", "abc"], True, "Exact match (Optimized)"),
        (optimized_solution.isSubsequence, ["abc", "abcde"], True, "Subsequence at start (Optimized)"),
        (optimized_solution.isSubsequence, ["abc", "deabc"], True, "Subsequence at end (Optimized)"),
        (optimized_solution.isSubsequence, ["abc", "ac"], False, "Target shorter than source (Optimized)"),
        (optimized_solution.isSubsequence, ["abcde", "ace"], False, "Source longer than target (Optimized)"),
        (optimized_solution.isSubsequence, ["", ""], True, "Both empty strings (Optimized)")
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution()
