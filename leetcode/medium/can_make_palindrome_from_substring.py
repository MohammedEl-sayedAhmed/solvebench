"""
1177. Can Make Palindrome from Substring
https://leetcode.com/problems/can-make-palindrome-from-substring/

You are given a string s and an array of queries, where queries[i] = [lefti, righti, ki].
We may rearrange the substring s[lefti...righti] for each query and then choose up to ki of them to replace with any lowercase English letter.

If the substring is possible to be a palindrome string after the operations above, the result of the query is true. Otherwise, the result is false.

Return a boolean array answer where answer[i] is the result of the ith query queries[i].

Note that each letter is counted individually for replacement, so if, for example s[lefti...righti] = "aaa", and ki = 2, we can only replace two of the letters. Also, note that no query modifies the initial string s.

Example 1:
Input: s = "abcda", queries = [[3,3,0],[1,2,0],[0,3,1],[0,3,2],[0,4,1]]
Output: [true, false, false, true, true]

Explanation:
queries[0]: substring = "d", is palindrome.
queries[1]: substring = "bc", is not palindrome.
queries[2]: substring = "abcd", is not palindrome after replacing only 1 character.
queries[3]: substring = "abcd", could be changed to "abba" which is palindrome.
queries[4]: substring = "abcda", could be changed to "abcba" which is palindrome.

Example 2:
Input: s = "lyb", queries = [[0,1,0],[2,2,1]]
Output: [false,true]

Constraints:
1 <= s.length, queries.length <= 10^5
0 <= lefti <= righti < s.length
0 <= ki <= s.length
s consists of lowercase English letters.
"""

import sys
import os
from collections import Counter

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from common.test_framework import run_tests

class Solution:
    def canMakePaliQueries(self, s: str, queries: list[list[int]]) -> list[bool]:
        
        # ------------------------ Brute Force Approach ------------------------
        # def can_form_palindrome_bruteforce(substring: str, k: int) -> bool:
        
        # n = len(s)
        # """
        # Brute Force Approach:
        # In this approach, we count the frequency of characters in the substring. A string can
        # be rearranged into a palindrome if, at most, one character has an odd frequency.
        
        # We need to check if we can replace characters such that no more than one character
        # remains with an odd frequency, meaning it can form a palindrome. If `k` replacements
        # are enough to fix the odd frequencies, return True.
        # """
        # # Count the frequency of characters in the substring using Counter
        # freq = Counter(substring)
        
        # # Calculate the number of characters with odd frequencies
        # odd_count = sum(1 for count in freq.values() if count % 2 != 0)
        
        # # If the odd count is 0 or 1 for odd-length substrings, it's a palindrome
        # # Otherwise, for even-length substrings, the odd count must be 0
        # # We can change `k` characters to fix the odd counts
        # return odd_count // 2 <= k
        
        
        
        # # ------------------------ Optimized Approach ------------------------
        # # Length of the string
        # n = len(s)
        
        # # Precompute the prefix frequency array
        # # prefix_freq[i][j] will store the frequency of character `chr(j + ord('a'))` in the substring s[0...i-1]
        # prefix_freq = [[0] * 26 for _ in range(n + 1)]
        
        # # Fill the prefix frequency array
        # for i in range(n):
        #     char_idx = ord(s[i]) - ord('a')
        #     for j in range(26):
        #         prefix_freq[i + 1][j] = prefix_freq[i][j]
        #     prefix_freq[i + 1][char_idx] += 1
        
        # # Helper function to count the number of odd frequencies in a substring s[left...right]
        # def count_odd_frequencies(left, right):
        #     odd_count = 0
        #     # Check the frequency of each character in the substring s[left...right]
        #     for i in range(26):
        #         freq_in_substring = prefix_freq[right + 1][i] - prefix_freq[left][i]
        #         if freq_in_substring % 2 != 0:
        #             odd_count += 1
        #     return odd_count
        
        # # Process each query
        # result = []
        # for left, right, k in queries:
        #     # Count the number of odd frequencies in the substring s[left...right]
        #     odd_count = count_odd_frequencies(left, right)
            
        #     # A string can be rearranged into a palindrome if odd_count / 2 <= k
        #     if odd_count // 2 <= k:
        #         result.append(True)
        #     else:
        #         result.append(False)

        # return result
        # Create prefix count array for each character
        n = len(s)
        prefix = [[0] * 26]  # Initialize with array of zeros for each letter
        
        # Build prefix sum array for character counts
        curr = [0] * 26
        for i in range(n):
            curr[ord(s[i]) - ord('a')] += 1
            prefix.append(curr[:])  # Make a copy of current counts
        
        def can_make_palindrome(left: int, right: int, k: int) -> bool:
            # Get character counts in the range [left, right]
            counts = [0] * 26
            for i in range(26):
                counts[i] = prefix[right + 1][i] - prefix[left][i]
            
            # Count characters with odd frequency
            odd_count = sum(1 for count in counts if count % 2 == 1)
            
            # For a string to be palindrome:
            # - All characters must appear even number of times, except possibly one
            # - Each replacement can fix 2 odd-frequency characters
            # - We need odd_count//2 replacements to make it palindrome
            return odd_count // 2 <= k
        
        # Process each query
        answer = []
        for left, right, k in queries:
            answer.append(can_make_palindrome(left, right, k))
        
        return answer
    
    
def test_solution():
    solution = Solution()

    # Define the test cases
    test_cases = [
        (solution.canMakePaliQueries, ["abcda", [[3, 3, 0], [1, 2, 0], [0, 3, 1], [0, 3, 2], [0, 4, 1]]], [True, False, False, True, True], "Example 1"),
        (solution.canMakePaliQueries, ["lyb", [[0, 1, 0], [2, 2, 1]]], [False, True], "Example 2"),
        (solution.canMakePaliQueries, ["abcba", [[0, 4, 0], [0, 4, 1]]], [True, True], "Already Palindrome"),
        (solution.canMakePaliQueries, ["aabbcc", [[0, 5, 2]]], [True], "Even length with sufficient replacements")
    ]

    # Run the tests
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution()
