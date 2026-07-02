"""
35. Search Insert Position
https://leetcode.com/problems/search-insert-position/

Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [1,3,5,6], target = 5
Output: 2

Example 2:
Input: nums = [1,3,5,6], target = 2
Output: 1

Example 3:
Input: nums = [1,3,5,6], target = 7
Output: 4

Constraints:
1 <= nums.length <= 10^4
-10^4 <= nums[i] <= 10^4
nums contains distinct values sorted in ascending order.
-10^4 <= target <= 10^4
"""

from common.test_framework import run_tests

class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        high = len(nums) - 1
        low = 0        
        # Handle cases where the target is not in the list and should be added at the beginning or end
        if target > nums[high]:
            return high + 1
        elif target < nums[low]:
            return 0
        
        while (high >= low):
            mid = low + (high - low) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return low
            
def test_solution():
    solution = Solution()

    test_cases = [
        (solution.searchInsert, [[1, 3, 5, 6], 5], 2, "Example 1"),
        (solution.searchInsert, [[1, 3, 5, 6], 2], 1, "Example 2"),
        (solution.searchInsert, [[1, 3, 5, 6], 7], 4, "Example 3"),
        (solution.searchInsert, [[1, 3, 5, 6], 0], 0, "Target less than all elements"),
        (solution.searchInsert, [[1, 3, 5, 6], 8], 4, "Target greater than all elements"),
        (solution.searchInsert, [[1, 3, 5, 6, 10], 9], 4, "Target between 6 and 10"),
        (solution.searchInsert, [[1, 2, 3, 4, 5], 4], 3, "Target in the middle"),
        (solution.searchInsert, [[1], 1], 0, "Single element, target is present"),
        (solution.searchInsert, [[1], 0], 0, "Single element, target is less than present"),
        (solution.searchInsert, [[1], 2], 1, "Single element, target is greater than present")
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution()
