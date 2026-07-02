"""
169. Majority Element
https://leetcode.com/problems/majority-element/

Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. 
You may assume that the majority element always exists in the array.

Example 1:
Input: nums = [3,2,3]
Output: 3

Example 2:
Input: nums = [2,2,1,1,1,2,2]
Output: 2

Constraints:
- n == nums.length
- 1 <= n <= 5 * 104
- -109 <= nums[i] <= 109

Follow-up: Could you solve the problem in linear time and in O(1) space?
"""

from common.test_framework import run_tests

class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        """
        Three approaches are implemented:
        1. Hash Map - O(n) time, O(n) space
        2. Sorting - O(n log n) time, O(1) space
        3. Boyer-Moore Voting - O(n) time, O(1) space
        """
        
        # Solution 1: Hash Map Approach
        # Time: O(n), Space: O(n)
        
        # count = {}
        # for num in nums:
        #     count[num] = count.get(num, 0) + 1
        # return max(count, key=count.get)
        
        # Solution 2: Sorting Approach
        # Time: O(n log n), Space: O(1)
        # After sorting, the majority element will always be located at the middle index of the sorted array. This is because the majority element appears more than half the time, so it will occupy the middle position when the array is sorted.
        # nums.sort()
        # mid_idx = len(nums) // 2
        # return nums[mid_idx]
        
        # Solution 3: Boyer-Moore Voting Algorithm
        # Time: O(n), Space: O(1)
        candidate = None
        count = 0
        
        for num in nums:
            if count == 0:
                candidate = num
            if num == candidate:
                count += 1
            else:
                count -= 1
                
        return candidate
            
def test_solution():
    solution = Solution()
    test_cases = [
        (solution.majorityElement, [[3, 2, 3]], 3, "Example 1"),
        (solution.majorityElement, [[2, 2, 1, 1, 1, 2, 2]], 2, "Example 2"),
        (solution.majorityElement, [[1]], 1, "Single element"),
        (solution.majorityElement, [[1, 1, 1, 1, 2, 2, 2]], 1, "Clear majority"),
        (solution.majorityElement, [[1, 2, 1, 2, 1]], 1, "Alternating with majority"),
        (solution.majorityElement, [[6, 5, 5]], 5, "Small array"),
        (solution.majorityElement, [[1, 1, 2, 1, 2, 2, 1]], 1, "Complex case"),
        (solution.majorityElement, [[-1, -1, -1, 1, 1, 1, -1]], -1, "Negative numbers"),
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution() 