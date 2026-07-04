// 26. Remove Duplicates from Sorted Array
// https://leetcode.com/problems/remove-duplicates-from-sorted-array/
//
// 
/*
Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.

Consider the number of unique elements in nums to be k​​​​​​​​​​​​​​. After removing duplicates, return the number of unique elements k.

The first k elements of nums should contain the unique numbers in sorted order. The remaining elements beyond index k - 1 can be ignored.

Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
If all assertions pass, then your solution will be accepted.

 

Example 1:

Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
Example 2:

Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
 

Constraints:

1 <= nums.length <= 3 * 104
-100 <= nums[i] <= 100
nums is sorted in non-decreasing order.
*/
//
// NOTE: the `package` line and the class name are set by the scaffolder
// (new.py) so they match the file's location and name.
package leetcode.easy;

import common.TestFramework;

import java.util.Arrays;

public class RemoveDuplicatesFromSortedArray {
    // Explain the approach. Time O(?), Space O(?).
    public int removeDuplicates(int[] nums) 
    {
        // int count = 1;

        // for (int i = 1; i < nums.length; i++)
        // {
        //     if (nums[i] == nums[i - 1])
        //     {
        //         continue;
        //     } 
        //     else
        //     {
        //         count++;
                
        //     }
        // }
        // return count;

        int l = 1;
        for(int r = 1; r < nums.length; r++)
        {
            if (nums[r] != nums[r - 1]) 
            {
                nums[l] = nums[r]; // Move it to the 'l' position
                l++;               // Advance 'l'
            }            
        }
        return l;
    }


    public static void main(String[] args) {
        RemoveDuplicatesFromSortedArray s = new RemoveDuplicatesFromSortedArray();
        TestFramework t = new TestFramework();

        // In-place problem: the answer is k plus the first k elements of the
        // mutated array (elements past k are "don't care", the _ in the prompt).
        // So mutate a named array, then compare copyOf(nums, k) to the expected —
        // that single check verifies both k == expected.length and the values,
        // exactly like LeetCode's custom judge. (Reuse this shape for #27
        // Remove Element, #80, Move Zeroes, and other in-place / return-k tasks.)
        int[] nums1 = {1, 1, 2};
        int k1 = s.removeDuplicates(nums1);
        t.check("Example 1", Arrays.copyOf(nums1, k1), new int[]{1, 2});

        int[] nums2 = {0, 0, 1, 1, 1, 2, 2, 3, 3, 4};
        int k2 = s.removeDuplicates(nums2);
        t.check("Example 2", Arrays.copyOf(nums2, k2), new int[]{0, 1, 2, 3, 4});

        System.exit(t.summary());
    }
}
