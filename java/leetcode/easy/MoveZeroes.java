// 283. Move Zeroes
// https://leetcode.com/problems/move-zeroes/
//
// Given an integer array nums, move all 0's to the end of it while maintaining
// the relative order of the non-zero elements.
//
// You must do this in-place without making a copy of the array.
//
// Example 1:
//   Input:  nums = [0,1,0,3,12]
//   Output: [1,3,12,0,0]
// Example 2:
//   Input:  nums = [0]
//   Output: [0]
//
// Constraints:
//   1 <= nums.length <= 10^4
//   -2^31 <= nums[i] <= 2^31 - 1
//
// Follow-up: minimize the total number of operations.
//
// NOTE: the `package` line and the class name are set by the scaffolder
// (new.py) so they match the file's location and name.
package leetcode.easy;

import common.TestFramework;

public class MoveZeroes {
    // Explain the approach. Time O(?), Space O(?).
    public void moveZeroes(int[] nums) {
        // TODO: move every 0 to the end, in place, keeping the non-zero order.
        int l = 0;
        int r = 0;
        for(int i = l; i < nums.length; i++)
        {
            if (nums[r] == 0)
            {
                r++;
            }
            else
            {
                int temp = nums[l];
                nums[l] = nums[r];
                nums[r] = temp;
                r++;
                l++;
            }
        }
    }

    public static void main(String[] args) {
        MoveZeroes s = new MoveZeroes();
        TestFramework t = new TestFramework();

        // In-place, void return: mutate a named array, then check the WHOLE
        // array against the expected result — every position is defined here
        // (no "don't care" tail like the return-k problems). Order matters
        // (zeros at the end, non-zeros keep their order), so use check.
        int[] nums1 = {0, 1, 0, 3, 12};
        s.moveZeroes(nums1);
        t.check("Example 1", nums1, new int[]{1, 3, 12, 0, 0});

        int[] nums2 = {0};
        s.moveZeroes(nums2);
        t.check("Example 2", nums2, new int[]{0});

        int[] nums3 = {1};
        s.moveZeroes(nums3);
        t.check("Example 2", nums3, new int[]{1});

        int[] nums4 = {1,0};
        s.moveZeroes(nums4);
        t.check("Example 2", nums4, new int[]{1,0});

        System.exit(t.summary());
    }
}
