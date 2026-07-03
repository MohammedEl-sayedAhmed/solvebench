// 125. Valid Palindrome
// https://leetcode.com/problems/valid-palindrome/
//
// A phrase is a palindrome if, after lowercasing and removing non-alphanumeric
// characters, it reads the same forwards and backwards. (Ported from Python.)
package leetcode.easy;

import common.TestFramework;

public class ValidPalindrome {
    // Two-pointer approach. Time O(n), Space O(1).

    // Use Character.isLetterOrDigit(c) in the loop 


    public boolean isPalindrome(String s) {
        int left = 0;
        int right = s.length() - 1;
        if (s == " ")
        {
            return true;
        }
        while(left < right)
        {
            char currFirst = s.charAt(left);
            char currlast = s.charAt(right);
           while(!Character.isLetterOrDigit(currFirst) && (left < right))
            {
                left++;
                currFirst = s.charAt(left);
            } 
            while(!Character.isLetterOrDigit(currlast) && (left < right))
            {
                right--;
                currlast = s.charAt(right);
            } 
            
            if(Character.toLowerCase(currFirst) != Character.toLowerCase(currlast))
            {
                return false;
            }
            
            left++;
            right--;
        }
        
        return true;
    }

    public static void main(String[] args) {
        ValidPalindrome s = new ValidPalindrome();
        TestFramework t = new TestFramework();

        t.check("Example 1", s.isPalindrome("A man, a plan, a canal: Panama"), true);
        t.check("Example 2", s.isPalindrome("race a car"), false);
        t.check("Space only", s.isPalindrome(" "), true);
        t.check("Numeric palindrome", s.isPalindrome("12321"), true);
        t.check("Mixed alphanumeric", s.isPalindrome("0P"), false);
        t.check("Underscore skipped", s.isPalindrome("ab_a"), true);
        t.check("Empty string", s.isPalindrome(""), true);
        t.check("Special characters only", s.isPalindrome("!@#$"), true);

        System.exit(t.summary());
    }
}
