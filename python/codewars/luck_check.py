"""
Luck Check
https://www.codewars.com/kata/luck-check

In some countries of former Soviet Union there was a belief about lucky tickets. A transport ticket of any sort was believed to possess luck if the sum of digits on the left half of its number was equal to the sum of digits on the right half. 

Your task is to write a function luck_check(str), which returns True if the argument is a string decimal representation of a lucky ticket number, or False for all other numbers. It should throw errors for empty strings or strings which don't represent a decimal number.

Examples:
003111    #             3 = 1 + 1 + 1
813372    #     8 + 1 + 3 = 3 + 7 + 2
17935     #         1 + 7 = 3 + 5  // if the length is odd, you should ignore the middle number when adding the halves.
56328116  # 5 + 6 + 3 + 2 = 8 + 1 + 1 + 6
"""

from common.test_framework import run_tests

def luck_check(ticket):
    # If we use left and right lists, we will use more space resulting in space complexity O(n)
    # If we use a running sum, we will optimize the space complexity resultin in space complexity O(1)
    # In all cases the time complexity is O(n)
    
    if ticket == "" or ticket.isdigit() == False:
        raise ValueError("Invalid type value should throw error")
    
    length = len(ticket)
    half = length // 2
    # left = []
    # right = []
    
    leftSum = 0
    rightSum = 0
    
    if length % 2 == 0:
        for i in range(0, half):
            # left.append(int(ticket[i]))
            leftSum += int(ticket[i])
            
        for i in range(half, length):
            # right.append(int(ticket[i]))
            rightSum += int(ticket[i])
    else:
        for i in range(0, half):
            # left.append(int(ticket[i]))
            leftSum += int(ticket[i])
        for i in range(half + 1, length):
            # right.append(int(ticket[i]))
            rightSum += int(ticket[i])
    
    # leftSum = sum(left)
    # rightSum = sum(right)
    
    if leftSum == rightSum:
        return True
    else:
        return False
        
def test_solution():
    test_cases = [
        (luck_check, ['5555'], True, "Test Case 1"),
        (luck_check, ['003111'], True, "Test Case 2"),
        (luck_check, ['543970707'], False, "Test Case 3"),
        (luck_check, ['439924'], False, "Test Case 4"),
        (luck_check, ['943294329932'], False, "Test Case 5"),
        (luck_check, ['000000'], True, "Test Case 6"),
        (luck_check, ['454319'], True, "Test Case 7"),
        (luck_check, ['1233499943'], False, "Test Case 8"),
        (luck_check, ['935336'], False, "Test Case 9")
        # New test cases for invalid inputs
        # (lambda: luck_check('6F43E8'), ValueError, "Invalid type value should throw error."),
        # (lambda: luck_check('1234 '), ValueError, "Invalid type value should throw error."),
        # (lambda: luck_check('124-21'), ValueError, "Invalid type value should throw error."),
        # (lambda: luck_check('124X212'), ValueError, "Invalid type value should throw error."),
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution() 