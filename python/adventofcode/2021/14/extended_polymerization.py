"""
Advent of Code - Day 14: Extended Polymerization
https://adventofcode.com/2021/day/14

The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization equipment 
that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves should even have the 
necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer template and 
a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result after repeating the pair 
insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are immediately adjacent, 
element C should be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.
Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are 
considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs 1749 times, 
C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most common element (B, 1749) and 
subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get 
if you take the quantity of the most common element and subtract the quantity of the least common element?
"""

from common.aoc import input_path
from collections import Counter, defaultdict

def polymerization_1(template, rules, steps):
    """
    Naive approach to perform the polymerization process.

    Args:
        template (str): The initial polymer template.
        rules (dict): The pair insertion rules.
        steps (int): The number of steps to perform.

    Returns:
        int: The difference between the most and least common elements after the given steps.

    Time Complexity: O(n * 2^k), where n is the length of the initial template and k is the number of steps.
    Space Complexity: O(n * 2^k), due to the exponential growth of the polymer string.
    """
    myList = []
    NumOfPair = len(template) - 1
    temp_template = template
    for k in range(steps):
        myList = []
        NumOfPair = len(temp_template) - 1
        for i in range(len(temp_template)):
            if i == NumOfPair:
                break
            pair = []
            pair.append(temp_template[i])
            pair.append(temp_template[i + 1])
            myList.append(pair)
        
        for i, pair in enumerate(myList):
            pair_str = pair[0] + pair[1]
            insert_char = rules[pair_str]
            new_str = pair[0] + insert_char
            myList[i] = new_str
            
        myList.append(temp_template[len(temp_template) - 1])    
        myList = "".join(myList)
        temp_template = myList
    
    element_count = Counter(myList)
    most_common = max(element_count.values())
    least_common = min(element_count.values())
    
    diff = most_common - least_common
    return diff

def polymerization_2(template, rules, steps):
    """
    Optimized approach to perform the polymerization process using pair counts.

    Args:
        template (str): The initial polymer template.
        rules (dict): The pair insertion rules.
        steps (int): The number of steps to perform.

    Returns:
        int: The difference between the most and least common elements after the given steps.

    Time Complexity: O(n + k * m), where n is the length of the initial template, k is the number of steps, and m is the number of unique pairs.
    Space Complexity: O(m), where m is the number of unique pairs.

    Note:
        The order of pairs in the dictionary does not affect the result in this problem. This is because the algorithm relies on counting
        occurrences of pairs and updating these counts based on the insertion rules. The order in which pairs are processed does not
        impact the final counts of elements or pairs. Python dictionaries maintain insertion order starting from version 3.7, but even
        if the order were different, the result would remain the same.
    """
    # Using defaultdict to automatically initialize missing keys with a default value (0 in this case)
    # This avoids the need to check if a key exists before updating its value
    pair_counts = defaultdict(int)
    element_counts = Counter(template)

    # Initialize pair counts from the template
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        pair_counts[pair] += 1

    # Perform the pair insertion process for the given number of steps
    for _ in range(steps):
        new_pair_counts = defaultdict(int)
        for pair, count in pair_counts.items():
            if pair in rules:
                insert_element = rules[pair]
                new_pair1 = pair[0] + insert_element
                new_pair2 = insert_element + pair[1]

                new_pair_counts[new_pair1] += count
                new_pair_counts[new_pair2] += count

                element_counts[insert_element] += count
            else:
                new_pair_counts[pair] += count

        # Update pair_counts to the new counts for the next step
        pair_counts = new_pair_counts

    most_common = max(element_counts.values())
    least_common = min(element_counts.values())
    return most_common - least_common

def solve_from_file(file_path):
    """Reads the input from a file and returns the template and rules."""
    full_file_path = input_path(__file__, file_path)
    
    with open(full_file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    template = lines[0]
    rules = {}
    for line in lines[1:]:
        if '->' in line:
            pair, insert = line.split(' -> ')
            rules[pair] = insert
    
    return template, rules

def test_solution():
    # Example usage
    template = "NNCB"
    rules = {
        "CH": "B",
        "HH": "N",
        "CB": "H",
        "NH": "C",
        "HB": "C",
        "HC": "B",
        "HN": "C",
        "NN": "C",
        "BH": "H",
        "NC": "B",
        "NB": "B",
        "BN": "B",
        "BB": "N",
        "BC": "B",
        "CC": "N",
        "CN": "C"
    }
    steps = 10
    result = polymerization_1(template, rules, steps)
    print(f"Test Case (polymerization_1): Difference between most and least common elements: {result}")

    result = polymerization_2(template, rules, steps)
    print(f"Test Case (polymerization_2): Difference between most and least common elements: {result}")

    # Test cases for checking the polymerization process
    test_cases = [
        # Test case format: (function, [args], expected_output, test_name)
        (polymerization_1, ["NNCB", rules, 10], 1588, "Example input (polymerization_1)"),
        (polymerization_2, ["NNCB", rules, 10], 1588, "Example input (polymerization_2)"),
    ]
    
    for func, args, expected, name in test_cases:
        result = func(*args)
        assert result == expected, f"Test {name} failed: expected {expected}, got {result}"
        print(f"Test {name} passed")

    # Read input from the input.txt file
    file_path = "input.txt"  # Ensure this matches the file name in your directory
    template, rules = solve_from_file(file_path)
    
    # Part 1 - Apply 10 steps of pair insertion
    part_1_result = polymerization_1(template, rules, 10)
    print(f"Part 1: Difference between most and least common elements: {part_1_result}")
    
    # Part 2 - Apply 40 steps of pair insertion
    part_2_result = polymerization_2(template, rules, 40)
    print(f"Part 2: Difference between most and least common elements: {part_2_result}")

if __name__ == "__main__":
    test_solution()