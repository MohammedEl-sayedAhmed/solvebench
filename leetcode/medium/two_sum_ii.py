"""
167. Two Sum II - Input Array Is Sorted
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two 
numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] 
and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers, index1 and index2, added by one as an integer array 
[index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may not use the same element twice.
Your solution must use only constant extra space.

Example 1:
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

Example 2:
Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

Example 3:
Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

Constraints:
- 2 <= numbers.length <= 3 * 10^4
- -1000 <= numbers[i] <= 1000
- numbers is sorted in non-decreasing order
- -1000 <= target <= 1000
- The tests are generated such that there is exactly one solution
"""

class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1
        
        while left < right:
            
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                return[left + 1, right + 1]
            elif current_sum > target:
                right -=1
            elif current_sum < target:
                left +=1
        
        return []
            
            
            



def test_solution():
    solution = Solution()
    
    test_cases = [
        ([2,7,11,15], 9, [1,2], "Example 1"),
        ([2,3,4], 6, [1,3], "Example 2"),
        ([-1,0], -1, [1,2], "Example 3"),
        ([1,2,3,4,5], 9, [4,5], "Sum at end"),
        ([1,2,3,4,5], 3, [1,2], "Sum at start"),
        ([1,2,3,4], 7, [3,4], "Middle numbers"),
        ([-2,-1,0,1], -1, [1,4], "Negative numbers"),
        ([1,1,2,2], 4, [3,4], "Duplicate numbers")
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for numbers, target, expected, test_name in test_cases:
        result = solution.twoSum(numbers, target)
        if result == expected:
            print(f"✅ {test_name} passed")
            passed_tests += 1
        else:
            print(f"\n❌ {test_name} failed")
            print(f"   Input: numbers = {numbers}, target = {target}")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")
    
    print(f"\nTest Results: {passed_tests}/{total_tests} passed")
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
    else:
        print(f"Failed {total_tests - passed_tests} tests")


if __name__ == "__main__":
    test_solution() 