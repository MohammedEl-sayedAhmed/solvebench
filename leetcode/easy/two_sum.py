"""
1. Two Sum
https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.
"""

class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """
        This solution uses a hash map to find the two indices of the numbers that add up to the target.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        num_to_idx = {}
        
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in num_to_idx:
                return [num_to_idx[complement], i]
            else:
                num_to_idx[nums[i]] = i
            

            


def test_solution():
    """
    Test function with various test cases to verify the solution.
    """
    solution = Solution()
    
    test_cases = [
        ([2,7,11,15], 9, [0,1], "Example 1"),
        ([3,2,4], 6, [1,2], "Example 2"),
        ([3,3], 6, [0,1], "Example 3"),
        ([1,2,3,4,5], 9, [3,4], "Sum at end"),
        ([1,2,3,4,5], 3, [0,1], "Sum at start"),
        ([1,2,3,4], 7, [2,3], "Middle numbers"),
        ([0,0,3,4], 0, [0,1], "Zeroes"),
        ([1,5,5,11], 10, [1,2], "Duplicate numbers")
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for nums, target, expected, test_name in test_cases:
        result = solution.twoSum(nums, target)
        if result == expected:
            print(f"✅ {test_name} passed")
            passed_tests += 1
        else:
            print(f"\n❌ {test_name} failed")
            print(f"   Input: nums = {nums}, target = {target}")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")
    
    print(f"\nTest Results: {passed_tests}/{total_tests} passed")
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
    else:
        print(f"Failed {total_tests - passed_tests} tests")


if __name__ == "__main__":
    test_solution() 