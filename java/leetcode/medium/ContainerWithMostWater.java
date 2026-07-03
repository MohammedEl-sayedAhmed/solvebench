// 11. Container With Most Water
// https://leetcode.com/problems/container-with-most-water/
//
// You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

// Find two lines that together with the x-axis form a container, such that the container contains the most water.

// Return the maximum amount of water a container can store.

// Notice that you may not slant the container.

// Input: height = [1,8,6,2,5,4,8,3,7]
// Output: 49
// Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
// Example 2:

// Input: height = [1,1]
// Output: 1




// NOTE: the `package` line and the class name are set by the scaffolder
// (new.py) so they match the file's location and name.
package leetcode.medium;

import common.TestFramework;

// import java.util.Collections;
// import java.util.ArrayList;
import java.math.*;

public class ContainerWithMostWater {
    // Explain the approach. Time O(?), Space O(?).
    public int maxArea(int[] height) 
    {
        int l = 0;
        int r = height.length - 1;
        int maxArea = 0;
        while (l < r) 
        {
            int currArea = Math.min(height[l] , height[r]) * (r - l);
            if (currArea > maxArea)
            {
                maxArea = currArea;
            }
    
            if (height[l] < height[r])
            {
                l++;
            }
            else
            {
                r--;
            }
        }
        return maxArea;
    }

    public static void main(String[] args) {
        ContainerWithMostWater s = new ContainerWithMostWater();
        TestFramework t = new TestFramework();

        t.check("Example 1", s.maxArea(new int [] {1,8,6,2,5,4,8,3,7}), 49);
        t.check("Example 2", s.maxArea(new int [] {1,1}), 1);

        System.exit(t.summary());
    }
}
