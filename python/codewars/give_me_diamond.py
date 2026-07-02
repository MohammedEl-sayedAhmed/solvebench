"""
Give me a Diamond
https://www.codewars.com/kata/give-me-a-diamond

Jamie is a programmer, and James' girlfriend. She likes diamonds, and wants a diamond string from James. Since James doesn't know how to make this happen, he needs your help.

Task:
You need to return a string that looks like a diamond shape when printed on the screen, using asterisk (*) characters. Trailing spaces should be removed, and every line must be terminated with a newline character (\n).

Return null/nil/None/... if the input is an even number or negative, as it is not possible to print a diamond of even or negative size.

Examples:
A size 3 diamond:
 *
***
 *
...which would appear as a string of " *\n***\n *\n"

A size 5 diamond:
  *
 ***
*****
 ***
  *
...that is:
"  *\n ***\n*****\n ***\n  *\n"
"""

from common.test_framework import run_tests

def diamond(n):
    if n % 2 == 0 or n <= 0:
        return None
    
    final_str = []
    if n % 2 == 0 or n < 0:
        return None
    
    for i in range(1, n - 1):
        # str = ""
        if i % 2 != 0:
            str = "*"
            spc = " "
            str = i * str
            spc = ((n - i) // 2) * spc
            final_str.append(spc + str)
            final_str.append("\n")  
                
    final_str.append( n * "*")
    final_str.append("\n")
   
    for j in range(n- 2, 0, -1):
        # str = ""
        if j % 2 != 0:
            str = "*"
            spc = " "
            str = j * str
            spc = ((n - j) // 2) * spc
            final_str.append(spc + str)
            final_str.append("\n")
            
    return "".join(final_str)

def test_solution():
    test_cases = [
        (diamond, [1], "*\n", "Test Case 1"),
        (diamond, [2], None, "Test Case 2"),
        (diamond, [3], " *\n***\n *\n", "Test Case 3"),
        (diamond, [5], "  *\n ***\n*****\n ***\n  *\n", "Test Case 4"),
        (diamond, [0], None, "Test Case 5"),  # Zero
        (diamond, [-3], None, "Test Case 6"),  # Negative number
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution()