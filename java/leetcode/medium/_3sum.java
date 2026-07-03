// 15. 3Sum
// https://leetcode.com/problems/3sum/
//
// Given an integer array nums, return all the triplets
// [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and
// nums[i] + nums[j] + nums[k] == 0.
//
// The solution set must not contain duplicate triplets.
//
// Example 1:
//   Input:  nums = [-1,0,1,2,-1,-4]
//   Output: [[-1,-1,2],[-1,0,1]]
// Example 2:
//   Input:  nums = [0,1,1]
//   Output: []
// Example 3:
//   Input:  nums = [0,0,0]
//   Output: [[0,0,0]]
//
// Constraints:
//   3 <= nums.length <= 3000
//   -10^5 <= nums[i] <= 10^5
//
// NOTE: the `package` line and the class name are set by the scaffolder
// (new.py) so they match the file's location and name.
package leetcode.medium;

import common.TestFramework;

import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

public class _3sum {
    // Explain the approach. Time O(?), Space O(?).
    public List<List<Integer>> threeSum(int[] nums) 
    {
        // TODO: return every unique triplet that sums to zero.
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>(); 

        int n = nums.length;

        for (int i = 0; i < n; i++)
        {
            int left = i + 1;
            int right = n - 1;

            if (i > 0 && nums[i] == nums[i - 1])
            {
                continue;
            }

            // Now it is reduced to a normal sorted 2 sum problem
            while (left < right) 
            {
                int sum = nums[i] + nums [left] + nums[right];

                if (sum == 0)
                {
                    res.add(Arrays.asList(nums[i],nums[left],nums[right]));
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    left++;
                    right--;
                }
                else if (sum < 0)
                {
                    left++;
                }
                else
                {
                    right--;
                }
                
            }

        }

        return res;
    }

    public static void main(String[] args) {
        _3sum s = new _3sum();
        TestFramework t = new TestFramework();

        // 3Sum output may be in any order, so use checkUnordered (it compares as
        // nested multisets). Return the triplets in whatever order you like.
        t.checkUnordered("Example 1", s.threeSum(new int[] {-1, 0, 1, 2, -1, -4}),
                List.of(List.of(-1, -1, 2), List.of(-1, 0, 1)));
        t.checkUnordered("Example 2", s.threeSum(new int[] {0, 1, 1}),
                List.of());
        t.checkUnordered("Example 3", s.threeSum(new int[] {0, 0, 0}),
                List.of(List.of(0, 0, 0)));

        System.exit(t.summary());
    }
}
