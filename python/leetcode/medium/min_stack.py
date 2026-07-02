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

from common.test_framework import run_tests

# Solution 1: Using Two Stacks (Optimal O(1) solution)
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

# Solution 2: Using a Doubly Linked List (for constant time `pop(i)` support)
# Time Complexity:
# Traversal: The method involves a traversal of the list to find the node at index i. This takes O(i) time.
# Modification: The removal of the node (updating pointers) happens in O(1) time since it only involves adjusting the pointers of the adjacent nodes.
# Thus, the overall time complexity of the popAt method is O(i), where i is the index of the node to be removed.
class Node:
    def __init__(self, value, current_min):
        self.value = value
        self.current_min = current_min
        self.next = None
        self.prev = None

class MinStackLinkedList:
    def __init__(self):
        self.head = None  
        self.tail = None 
        
    def push(self, val: int) -> None:
        
        # Push a new value onto the stack, updating the minimum value as we go.
        # If the tail is None (empty stack), the new min is the value itself
        if not self.tail:
            new_min = val
        # If the tail exists, we compare the current value with the current minimum
        else:
            current_min = self.tail.current_min
            new_min = min(val,current_min)
        
        new_node = Node(val, new_min)
        
        # This is the first node to be inserted in the linked list
        if not self.head:
            self.head = self.tail = new_node
        # Not the first node in the linked list
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
    def pop(self) -> None:
        # Pop the top value from the stack.

        # Empty linked list
        if not self.tail:
            return
        # LL has only 1 node
        if self.tail == self.head:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
    
    def popAt(self, i: int) -> None:
        # Pop a value at a specific index i in constant time.
        current = self.head
        for _ in range(i):
            if current is None:
                return  # index out of bounds
            current = current.next
            
        # Shift the prev and next pointers
        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev
            
        # We need to check if it was the head or the tail of the list:
        if current == self.head:
            self.head = current.next
        if current == self.tail:
            self.tail = current.prev
    
    def top(self) -> int:
        if self.tail:
            return self.tail.value
        else:
            return None
        
    def getMin(self) -> int:
        if self.tail:
            return self.tail.current_min
        else:
            return None
        
def test_solution():
    # Create instances of both solutions
    min_stack = MinStack()
    min_stack_LL = MinStackLinkedList()

    # Test cases to evaluate both MinStack implementations
    test_cases = [
        # Test the two-stack solution
        (min_stack.push, [-2], None, "Push -2"),
        (min_stack.push, [0], None, "Push 0"),
        (min_stack.push, [-3], None, "Push -3"),
        (min_stack.getMin, [], -3, "Get Min after pushing -3"),
        (min_stack.pop, [], None, "Pop"),
        (min_stack.top, [], 0, "Top after pop"),
        (min_stack.getMin, [], -2, "Get Min after pop"),
        (min_stack.push, [5], None, "Push 5"),
        (min_stack.push, [3], None, "Push 3"),
        (min_stack.getMin, [], -2, "Get Min after pushing 3"),
        (min_stack.pop, [], None, "Pop"),
        (min_stack.getMin, [], -2, "Get Min after popping"),

        # Test the doubly linked list solution
        (min_stack_LL.push, [-2], None, "Push -2 (LinkedList)"),
        (min_stack_LL.push, [0], None, "Push 0 (LinkedList)"),
        (min_stack_LL.push, [-3], None, "Push -3 (LinkedList)"),
        (min_stack_LL.getMin, [], -3, "Get Min after pushing -3 (LinkedList)"),
        (min_stack_LL.pop, [], None, "Pop (LinkedList)"),
        (min_stack_LL.top, [], 0, "Top after pop (LinkedList)"),
        (min_stack_LL.getMin, [], -2, "Get Min after pop (LinkedList)"),
        (min_stack_LL.push, [5], None, "Push 5 (LinkedList)"),
        (min_stack_LL.push, [3], None, "Push 3 (LinkedList)"),
        (min_stack_LL.getMin, [], -2, "Get Min after pushing 3 (LinkedList)"),
        (min_stack_LL.pop, [], None, "Pop (LinkedList)"),
        (min_stack_LL.getMin, [], -2, "Get Min after popping (LinkedList)"),
    ]

    # Run the test cases using the `run_tests` function
    run_tests(test_cases)

if __name__ == "__main__":
    test_solution()
