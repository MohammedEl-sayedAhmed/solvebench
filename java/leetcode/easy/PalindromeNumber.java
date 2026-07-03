// 9. Palindrome Number
// https://leetcode.com/problems/palindrome-number/
//
// Given an integer x, return true if x is a palindrome, and false otherwise.

// Example 1:

// Input: x = 121
// Output: true
// Explanation: 121 reads as 121 from left to right and from right to left.
// Example 2:

// Input: x = -121
// Output: false
// Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
// Example 3:

// Input: x = 10
// Output: false
// Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
 

// Constraints:

// -231 <= x <= 231 - 1
 

// Follow up: Could you solve it without converting the integer to a string?


// This can be solved with 2 pointers
package leetcode.easy;

import common.TestFramework;

public class PalindromeNumber {
    // Approach: reverse only the SECOND half of the digits (no string
    // conversion) and compare it with the first half. Time O(log10 n) — we
    // process about half the digits — and Space O(1).
    //
    // Alternative (kept for reference): a string two-pointer scan, which is
    // simpler but O(n) time and O(n) space for the string:
    // public boolean isPalindrome(int x)
    // {
    //     String[] str_x = String.valueOf(x).split("");
    //     int l = 0;
    //     int r = str_x.length - 1;
        
    //     while (l < r) 
    //     {
    //         if(!str_x[l].equals(str_x[r]))
    //         {
    //             return false;
    //         }
    //         l++;
    //         r--;

    //         if(l >= r)
    //         {
    //             return true;
    //         }
    //     }

    //     return false;
    // }



    // Solve without converting int to STR
    // Edge case 1: Any negative number is false
    // Edge case 2: if it is multiple of 10, 10, 20, 30, etc
    // Edge case 3: if x is 0, it should be true
    // To make faster, we only need to reverse second half and check it with first half 
    // Key equation of this, to get the last digit from a number is to num % 10 
    // 123 % 10 leaves a remainder of 3
    // 45 % 10 leaves a remainder of 5
    // then we can like remove it so we end up of the full number without the last digit; 
    // so 123 becomes 120, so that when we do 120 % 10 we get 2 
    // and so on

    public boolean isPalindrome(int x) 
    {
        if (x < 0 || (x % 10 == 0 && x != 0) )
        {
            return false;
        }

        int reversedHalf = 0;

        while (x > reversedHalf) 
        {
            reversedHalf = (reversedHalf * 10) + (x % 10);
            x = x /10;
            
        }

        // Even number of digits: x ends up equal to reversedHalf.
        // Odd number of digits: the middle digit lands in reversedHalf's last
        // place, so drop it with /10 before comparing.

        return x == reversedHalf || x == reversedHalf /10;

    }

    public static void main(String[] args) {
        PalindromeNumber s = new PalindromeNumber();
        TestFramework t = new TestFramework();

        t.check("Example 1", s.isPalindrome(121), true);
        t.check("Example 2", s.isPalindrome(-121), false);
        t.check("Example 3", s.isPalindrome(10), false);
        t.check("Example 3", s.isPalindrome(0), true);
        t.check("Example 4", s.isPalindrome(1221), true);
        t.check("Example 5", s.isPalindrome(12321), true);

        System.exit(t.summary());
    }
}
