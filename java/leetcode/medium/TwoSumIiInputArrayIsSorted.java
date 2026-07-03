// 167. Two Sum II - Input Array Is Sorted
// https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
//
// Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

// Return the indices of the two numbers index1 and index2, each incremented by one, as an integer array [index1, index2] of length 2.

// The tests are generated such that there is exactly one solution. You may not use the same element twice.

// Your solution must use only constant extra space.

 

// Example 1:

// Input: numbers = [2,7,11,15], target = 9
// Output: [1,2]
// Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
// Example 2:

// Input: numbers = [2,3,4], target = 6
// Output: [1,3]
// Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
// Example 3:

// Input: numbers = [-1,0], target = -1
// Output: [1,2]
// Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

//
// Constraints:

// 2 <= numbers.length <= 3 * 104
// -1000 <= numbers[i] <= 1000
// numbers is sorted in non-decreasing order.
// -1000 <= target <= 1000

// The tests are generated such that there is exactly one solution.


// NOTE: the `package` line and the class name are set by the scaffolder


package leetcode.medium;

import common.TestFramework;

import java.util.HashMap;

public class TwoSumIiInputArrayIsSorted {
    // Explain the approach. Time O(?), Space O(?).
    public int[] twoSum(int[] numbers, int target) 
    {
        HashMap<Integer, Integer> seen = new HashMap<>();

        for(int i = 0; i < numbers.length; i++)
        {
            int complement = target - numbers[i];

            if(seen.containsKey(complement))
            {
                int [] indices = new int[] {seen.get(complement) + 1, i + 1};
                return indices;
            }
            seen.put(numbers[i], i);
        }

        return new int[] {};    
    }

    public static void main(String[] args) {
        TwoSumIiInputArrayIsSorted s = new TwoSumIiInputArrayIsSorted();
        TestFramework t = new TestFramework();

        t.check("Example 1", s.twoSum(new int[]{2,7,11,15},9), new int[] {1,2});
        t.check("Example 1", s.twoSum(new int[]{2,3,4},6), new int[] {1,3});
        t.check("Example 1", s.twoSum(new int[]{-1,0},-1), new int[] {1,2});


        System.exit(t.summary());
    }
}
