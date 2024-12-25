"""
88. Merge Sorted Array
https://leetcode.com/problems/merge-sorted-array/

You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.

Example 1:
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.

Example 2:
Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
Explanation: The arrays we are merging are [1] and [].
The result of the merge is [1].

Example 3:
Input: nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
Explanation: The arrays we are merging are [] and [1].
The result of the merge is [1].
Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.

Constraints:
nums1.length == m + n
nums2.length == n
0 <= m, n <= 200
1 <= m + n <= 200
-10^9 <= nums1[i], nums2[j] <= 10^9
"""

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from common.test_framework import run_tests
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # Initialize pointers
        i, j, k = m - 1, n - 1, m + n - 1
        
        # Merge from the end of nums1 and nums2
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
        
        # If there are any remaining elements in nums2, copy them
        while j >= 0:
            nums1[k] = nums2[j]
            j -= 1
            k -= 1
        





def test_solution():
    solution = Solution()

    # Test cases to verify correctness
    test_cases = [
        # Example 1
        (solution.merge, [[1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3], [1, 2, 2, 3, 5, 6], "Example 1"),
        # Example 2
        (solution.merge, [[1], 1, [], 0], [1], "Example 2"),
        # Example 3
        (solution.merge, [[0], 0, [1], 1], [1], "Example 3"),
        # nums1 is initially empty
        (solution.merge, [[0, 0, 0, 0], 0, [1, 2, 3, 4], 4], [1, 2, 3, 4], "nums1 is initially empty"),
        # nums1 has larger values initially
        (solution.merge, [[9, 10, 11, 0, 0, 0], 3, [4, 5, 6], 3], [4, 5, 6, 9, 10, 11], "nums1 has larger values initially"),
        # nums1 is initially all zeros
        (solution.merge, [[0, 0, 0, 0, 0, 0], 0, [1, 2, 3, 4, 5, 6], 6], [1, 2, 3, 4, 5, 6], "nums1 is initially all zeros")
    ]
    
    def merge_wrapper(*args):
        nums1_copy = args[0][:]  # Create a copy for the test
        solution.merge(nums1_copy, *args[1:]) # unpack additional parameters from args
        return nums1_copy  # Return the modified copy

    modified_test_cases = []
    for func, args, expected, test_name in test_cases:
        modified_test_cases.append((merge_wrapper, args, expected, test_name))

    run_tests(modified_test_cases) # IMPORTANT:  Pass in the MODIFIED test cases.

    # Run the tests
    # run_tests(test_cases)


if __name__ == "__main__":
    test_solution()
