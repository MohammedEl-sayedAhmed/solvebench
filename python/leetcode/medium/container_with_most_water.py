"""
11. Container With Most Water
https://leetcode.com/problems/container-with-most-water/

You are given an integer array height of length n. There are n vertical lines drawn such that the two 
endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.
Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Example 1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. 
In this case, the max area of water (blue section) the container can contain is 49.

Example 2:
Input: height = [1,1]
Output: 1

Constraints:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4
"""

from common.test_framework import run_tests

class Solution:
    def maxArea(self, height: list[int]) -> int:
        """
        Two approaches are implemented:
        1. Brute Force - O(n²) time, O(1) space
        2. Two Pointer - O(n) time, O(1) space
        """
        
        # Solution 1: Brute Force Approach
        # Time: O(n²), Space: O(1)
        # max_area = 0
        # for left in range(len(height)):
        #     for right in range(left + 1, len(height)):
        #         area = min(height[left], height[right]) * (right - left)
        #         max_area = max(area, max_area)
        # return max_area

        # Solution 2: Two Pointer Approach
        # Time: O(n), Space: O(1)
        left = 0
        right = len(height) - 1
        max_area = 0
        
        while left < right:
            # Calculate current area
            area = min(height[left], height[right]) * (right - left)
            max_area = max(area, max_area)
            
            # Move pointer of the smaller height inward
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
                
        return max_area
    
def test_solution():
    solution = Solution()

    test_cases = [
        (solution.maxArea, [[1, 8, 6, 2, 5, 4, 8, 3, 7]], 49, "Example 1"),
        (solution.maxArea, [[1, 1]], 1, "Example 2"),
        (solution.maxArea, [[4, 3, 2, 1, 4]], 16, "Equal heights at ends"),
        (solution.maxArea, [[1, 2, 4, 3]], 4, "Small array"),
        (solution.maxArea, [[1, 8, 6, 2, 5, 4, 8, 25, 7]], 49, "Large height in middle"),
        (solution.maxArea, [[1, 1, 1, 1]], 3, "Equal heights"),
        (solution.maxArea, [[1, 2, 3, 4, 5]], 6, "Increasing heights"),
        (solution.maxArea, [[5, 4, 3, 2, 1]], 6, "Decreasing heights")
    ]

    run_tests(test_cases)
if __name__ == "__main__":
    test_solution()