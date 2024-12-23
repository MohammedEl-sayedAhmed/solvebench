"""
155. Min Stack
https://leetcode.com/problems/min-stack/

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:

MinStack() initializes the stack object.
void push(int val) pushes the element val onto the stack.
void pop() removes the element on the top of the stack.
int top() gets the top element of the stack.
int getMin() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

Example 1:
Input
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

Output
[null,null,null,null,-3,null,0,-2]

Explanation:
MinStack minStack = new MinStack();
minStack.push(-2);    // stack = [-2]
minStack.push(0);     // stack = [-2, 0]
minStack.push(-3);    // stack = [-2, 0, -3]
minStack.getMin();    // return -3
minStack.pop();       // stack = [-2, 0]
minStack.top();       // return 0
minStack.getMin();    // return -2

Constraints:
-231 <= val <= 231 - 1
Methods pop, top and getMin operations will always be called on non-empty stacks.
At most 3 * 104 calls will be made to push, pop, top, and getMin.

"""
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from common.test_framework import run_tests

class MinStack:
    def __init__(self):
        # Initialize the stack and the min_stack.
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        # Push the value onto the stack and update the min_stack.
        self.stack.append(val)
        
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(val, self.min_stack[-1]))
        
    
    def pop(self) -> None:
        # Pop the value from the stack and also from the min_stack if it's the minimum value.
        self.stack.pop()
        self.min_stack.pop()
        
    
    def top(self) -> int:
        # Return the top value from the stack.
        return self.stack[-1]
       
    
    def getMin(self) -> int:
        # Return the minimum value from the min_stack (top element).
        return self.min_stack[-1]
       

def test_solution():
    min_stack = MinStack()
    
    # Test cases to evaluate the MinStack implementation
    test_cases = [
        # First test case
        (min_stack.push, [-2], None, "Push -2"),
        (min_stack.push, [0], None, "Push 0"),
        (min_stack.push, [-3], None, "Push -3"),
        (min_stack.getMin, [], -3, "Get Min after pushing -3"),
        (min_stack.pop, [], None, "Pop"),
        (min_stack.top, [], 0, "Top after pop"),
        (min_stack.getMin, [], -2, "Get Min after pop"),

        # Edge cases
        (min_stack.push, [5], None, "Push 5"),
        (min_stack.push, [3], None, "Push 3"),
        (min_stack.getMin, [], -2, "Get Min after pushing 3"),
        (min_stack.pop, [], None, "Pop"),
        (min_stack.getMin, [], -2, "Get Min after popping"),
    ]
    
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution()
