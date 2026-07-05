// 1. Two Sum
// https://leetcode.com/problems/two-sum/
//
// Given an array of integers nums and an integer target, return indices of the
// two numbers such that they add up to target. (Ported from the Python solution.)
package leetcode.easy;

import common.TestFramework;

import java.util.HashMap;
import java.util.Map;

public class TwoSum {
    // Hash map approach. Time O(n), Space O(n).
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>(); // better to declare variables using the interface (Map) and initialize them using the implementation (HashMap).
        for (int i =0; i < nums.length; i++)
        {
            int complement = target - nums[i];

            if(map.containsKey(complement))
            {
                int[] indices = new int[]{map.get(complement), i};
                return indices;
            }

            map.put(nums[i], i);
        }

        return new int[] {};
    }

    public static void main(String[] args) {
        TwoSum s = new TwoSum();
        TestFramework t = new TestFramework();

        t.check("Example 1", s.twoSum(new int[] {2, 7, 11, 15}, 9), new int[] {0, 1});
        t.check("Example 2", s.twoSum(new int[] {3, 2, 4}, 6), new int[] {1, 2});
        t.check("Example 3", s.twoSum(new int[] {3, 3}, 6), new int[] {0, 1});
        t.check("Sum at end", s.twoSum(new int[] {1, 2, 3, 4, 5}, 9), new int[] {3, 4});
        t.check("Sum at start", s.twoSum(new int[] {1, 2, 3, 4, 5}, 3), new int[] {0, 1});
        t.check("Zeroes", s.twoSum(new int[] {0, 0, 3, 4}, 0), new int[] {0, 1});
        t.check("Duplicate numbers", s.twoSum(new int[] {1, 5, 5, 11}, 10), new int[] {1, 2});

        System.exit(t.summary());
    }
}
