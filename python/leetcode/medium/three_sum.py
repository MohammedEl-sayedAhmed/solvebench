"""
15. 3Sum
https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that 
i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.

Constraints:
- 3 <= nums.length <= 3000
- -105 <= nums[i] <= 105
"""

from common.test_framework import run_tests

class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        """
        Two approaches are implemented:
        1. Brute Force - O(n³) time, O(1) space
        2. Two Pointer - O(n²) time, O(1) space
        """
        
        # Solution 1: Brute Force Approach (Time Limit Exceeded)
        # Time: O(n³), Space: O(1)
        # res = set()
        # for i in range(len(nums)):
        #     for j in range(i+1, len(nums)):
        #         for k in range(j+1, len(nums)):
        #             sum = nums[i] + nums[j] + nums[k]
        #             if sum == 0:
        #                 res.add(tuple(sorted([nums[i], nums[j], nums[k]])))
        # return [list(x) for x in res]
                    
        # Solution 2: Two Pointer Approach
        # Time: O(n²), Space: O(1)
        
        # We can sort the array to handle duplicates and ease the iteration of pointers
        nums.sort()
        res = []
        
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            # normal 2 sum problem, using pointers
            left = i + 1
            right = len(nums) - 1
            
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                
                if total == 0:
                    res.append([nums[i], nums[left], nums[right]])
                    left += 1
                    while nums[left] == nums[left-1] and left < right:
                        left += 1
                elif total > 0:
                    right -= 1
                else:
                    left += 1
        return res
                
def test_solution():
   solution = Solution()
   
   test_cases = [
       (solution.threeSum, [[-1, 0, 1, 2, -1, -4]], [[-1, -1, 2], [-1, 0, 1]], "Example 1"),
       (solution.threeSum, [[0, 1, 1]], [], "Example 2"),
       (solution.threeSum, [[0, 0, 0]], [[0, 0, 0]], "Example 3"),
       (solution.threeSum, [[-2, 0, 1, 1, 2]], [[-2, 0, 2], [-2, 1, 1]], "Multiple valid triplets"),
       (solution.threeSum, [[1, 2, 3, 4, 5]], [], "No valid triplets"),
       (solution.threeSum, [[-1, -1, -1, 2, 2, 2]], [[-1, -1, 2]], "Duplicate numbers"),
       (solution.threeSum, [[0, 0, 0, 0]], [[0, 0, 0]], "Multiple zeros")
   ]
   
   run_tests(test_cases)
if __name__ == "__main__":
   test_solution()