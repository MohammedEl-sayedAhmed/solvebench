// 125. Valid Palindrome
// https://leetcode.com/problems/valid-palindrome/
//
// A phrase is a palindrome if, after lowercasing and removing non-alphanumeric
// characters, it reads the same forwards and backwards. (Ported from Python.)
package leetcode.easy;

import common.TestFramework;

public class ValidPalindrome {
    // Two-pointer approach. Time O(n), Space O(1).
    public boolean isPalindrome(String s) {
        int left = 0;
        int right = s.length() - 1;
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
                left++;
            }
            while (right > left && !Character.isLetterOrDigit(s.charAt(right))) {
                right--;
            }
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
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
