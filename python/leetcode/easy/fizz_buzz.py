"""
412. Fizz Buzz
https://leetcode.com/problems/fizz-buzz/

Given an integer n, return a string array answer (1-indexed) where:

answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
answer[i] == "Fizz" if i is divisible by 3.
answer[i] == "Buzz" if i is divisible by 5.
answer[i] == i (as a string) if none of the above conditions are true.

Example 1:
Input: n = 3
Output: ["1","2","Fizz"]

Example 2:
Input: n = 5
Output: ["1","2","Fizz","4","Buzz"]

Example 3:
Input: n = 15
Output: ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]

Constraints:
1 <= n <= 10^4
"""

from common.test_framework import run_tests
class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        result = []
        for i in range(1,n + 1):
            if i % 3 == 0 and i % 5 == 0 :
                result.append("FizzBuzz")
            elif i % 3 == 0:
                result.append("Fizz")
            elif i % 5 == 0:
                result.append("Buzz")
            else:
                result.append(str(i))
        return result
            
def test_solution():
    solution = Solution()
    
    test_cases = [
        (solution.fizzBuzz, [3], ["1", "2", "Fizz"], "Example 1"),
        (solution.fizzBuzz, [5], ["1", "2", "Fizz", "4", "Buzz"], "Example 2"),
        (solution.fizzBuzz, [15], ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"], "Example 3"),
        (solution.fizzBuzz, [1], ["1"], "Single number"),
        (solution.fizzBuzz, [2], ["1", "2"], "Two numbers"),
        (solution.fizzBuzz, [30], ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz", "16", "17", "Fizz", "19", "Buzz", "Fizz", "22", "23", "Fizz", "Buzz", "26", "Fizz", "28", "29", "FizzBuzz"], "Up to 30")
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution() 