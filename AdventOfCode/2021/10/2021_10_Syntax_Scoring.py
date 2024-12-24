"""
Advent of Code - Day 10: Syntax Scoring
https://adventofcode.com/2021/day/10

The navigation subsystem syntax is made of several lines containing chunks. There are one or more chunks on each line, 
and chunks contain zero or more other chunks. Adjacent chunks are not separated by any delimiter; if one chunk stops, 
the next chunk (if any) can immediately start. Every chunk must open and close with one of four legal pairs of matching characters:

- If a chunk opens with (, it must close with ).
- If a chunk opens with [, it must close with ].
- If a chunk opens with {, it must close with }.
- If a chunk opens with <, it must close with >.

Your task is to find and discard the corrupted lines first.

A corrupted line is one where a chunk closes with the wrong character - that is, where the characters it opens and closes with 
do not form one of the four legal pairs listed above.

For each corrupted line, calculate the syntax error score based on the first illegal character:
- ): 3 points
- ]: 57 points
- }: 1197 points
- >: 25137 points

Example input:
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
[[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
[{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
[<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
<{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.

Solution:
We need to calculate the total syntax error score for the corrupted lines.
"""

import sys
import os

# Add the root directory to the Python path (for testing purposes)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from common.test_framework import run_tests

"""
Explanation:

- **`syntax_error_score()` method**:
  1. This method processes each line in the input.
  2. For each line, it checks if the characters are correctly paired by using a stack.
  3. If a mismatch occurs (i.e., a corrupted line), the corresponding error score is added to the total.
  4. It uses the `opening` and `closing` dictionaries to verify matching pairs of characters and `error_scores` to map illegal characters to their error scores.
  5. The algorithm runs in O(n) time complexity, where `n` is the total number of characters in the input lines.

- **Test Cases**:
  - The test cases evaluate the solution with the provided example input and additional edge cases.
  - The example input calculates the total syntax error score as 26397, which is the correct answer based on the puzzle description.
"""

class Solution:
    def part_1(self, lines):
        """
        Function to calculate the total syntax error score for the corrupted lines.

        The approach involves:
        1. Iterating over each line and checking if it is corrupted.
        2. When encountering the first corrupted character, it adds the corresponding points to the total score.
        
        Time Complexity: O(n), where `n` is the total number of characters in all lines.
        """
        # Mapping of corrupted character to their error scores
        error_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
        
        # Define matching pairs for valid chunks
        opening = {'(': ')', '[': ']', '{': '}', '<': '>'}
        closing = {')': '(', ']': '[', '}': '{', '>': '<'}
        
        total_score = 0            
        
        for line in lines:
            stack = []
            for char in line:
                if char in opening:  # If it's an opening character, push it onto the stack
                    stack.append(char)
                elif char in closing:  # If it's a closing character
                    # Check if the top of the stack has the matching opening character (corresponding close)
                    if not stack or stack[-1] != closing[char]:
                        total_score += error_scores[char]  # Add error points if mismatched
                        break
                    stack.pop()  # If the character is valid, pop the stack
        return total_score
    
    
    def part_2(self, lines):
        """
        Function to calculate the middle score of the completion strings for incomplete lines.
        """
        opening = {'(': ')', '[': ']', '{': '}', '<': '>'}
        closing = {')': '(', ']': '[', '}': '{', '>': '<'}
        autocomplete_scores = {')': 1, ']': 2, '}': 3, '>': 4}
        
        scores = []
        
        for line in lines:
            stack = []
            is_corrupted = False
            for char in line:
                if char in opening:
                    stack.append(char)
                elif char in closing:
                    if not stack or stack[-1] != closing[char]:
                        is_corrupted = True
                        break
                    stack.pop()

            if not is_corrupted:  # Only process incomplete lines
                # Calculate the autocomplete score for the remaining open chunks
                completion_string = ""
                while stack:
                    open_char = stack.pop()
                    completion_string += opening[open_char]  # Add the corresponding closing character

                # Now, calculate the score for the completion string
                score = 0
                for char in completion_string:
                    score = score * 5 + autocomplete_scores[char]
                
                scores.append(score)

        # Sort the scores and return the middle score
        scores.sort()
        return scores[len(scores) // 2]


def solve_from_file(file_path):
    """Reads the input from a file and returns the lines."""
    # Ensure the correct file path based on the script's location
    script_dir = os.path.dirname(os.path.realpath(__file__))
    full_file_path = os.path.join(script_dir, file_path)
    
    with open(full_file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def test_solution():
    solution = Solution()
    
    # # Test cases for checking the syntax error score calculation
    # test_cases = [
    #     # # Test case format: (function, [args], expected_output, test_name)
    #     # (solution.part_2, [INPUT HERE], OUTPUT, "Part 2 Example input") Template, our case the input is list of str ["", "", ""]
        
    #     (solution.part_1, [["[({(<(())[]>[[{[]{<()<>", 
    #                                    "[(()[<>])]({[<{<<[]>>(", 
    #                                    "{([(<{}[<>[]}>{[]{[(<()>", 
    #                                    "[[<[([]))<([[{}[[()]]]", 
    #                                    "[{[{({}]{}}([{[{{{}}([]", 
    #                                    "{<[[]]>}<{[{[{[]{()[[[]", 
    #                                    "[<(<(<(<{}))><([]([]()", 
    #                                    "<{([([[(<>()){}]>(<<{{", 
    #                                    "<{([{{}}[<[[[<>{}]]]>[]]"]], 26397, "Part 1 Example input"),
    #     # Additional test case for edge case scenarios
    #     (solution.part_2, [["[({(<(())[]>[[{[]{<()<>>",
    #                         "[(()[<>])]({[<{<<[]>>(",
    #                         "(((({<>}<{<{<>}{[]{[]{}",
    #                         "{<[[]]>}<{[{[{[]{()[[[]",
    #                         "<{([{{}}[<[[[<>{}]]]>[]]"]], 288957, "Part 2 Example input")

    # ]
    # run_tests(test_cases)
    
    # Read input from the input.txt file
    file_path = "input.txt"  # Ensure this matches the file name in your directory
    lines = solve_from_file(file_path)
    
    # Part 1 - Calculate the syntax error score for corrupted lines
    part_1_result = solution.part_1(lines)
    print(f"Part 1: Total syntax error score: {part_1_result}")

    # Part 2 - Calculate the middle score for autocomplete strings
    part_2_result = solution.part_2(lines)
    print(f"Part 2: Middle autocomplete score: {part_2_result}")


if __name__ == "__main__":
    test_solution()



