// 412. Fizz Buzz
// https://leetcode.com/problems/fizz-buzz/
//
// Return a string array: "Fizz" for multiples of 3, "Buzz" for multiples of 5,
// "FizzBuzz" for both, else the number. (Ported from the Python solution.)
package leetcode.easy;

import common.TestFramework;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class FizzBuzz {
    public List<String> fizzBuzz(int n) {
        List<String> result = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            if (i % 3 == 0 && i % 5 == 0) {
                result.add("FizzBuzz");
            } else if (i % 3 == 0) {
                result.add("Fizz");
            } else if (i % 5 == 0) {
                result.add("Buzz");
            } else {
                result.add(String.valueOf(i));
            }
        }
        return result;
    }

    public static void main(String[] args) {
        FizzBuzz s = new FizzBuzz();
        TestFramework t = new TestFramework();

        t.check("Example 1", s.fizzBuzz(3), Arrays.asList("1", "2", "Fizz"));
        t.check("Example 2", s.fizzBuzz(5), Arrays.asList("1", "2", "Fizz", "4", "Buzz"));
        t.check("Example 3", s.fizzBuzz(15), Arrays.asList(
                "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
                "11", "Fizz", "13", "14", "FizzBuzz"));
        t.check("Single number", s.fizzBuzz(1), Arrays.asList("1"));
        t.check("Two numbers", s.fizzBuzz(2), Arrays.asList("1", "2"));

        System.exit(t.summary());
    }
}
