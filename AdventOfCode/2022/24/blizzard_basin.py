"""
Advent of Code - Day 24: Blizzard Basin
https://adventofcode.com/2022/day/24

With everything replanted for next year (and with elephants and monkeys to tend the grove), you and the Elves leave for the extraction point.

Partway up the mountain that shields the grove is a flat, open area that serves as the extraction point. It's a bit of a climb, but nothing the expedition can't handle.

At least, that would normally be true; now that the mountain is covered in snow, things have become more difficult than the Elves are used to.

As the expedition reaches a valley that must be traversed to reach the extraction site, you find that strong, turbulent winds are pushing small blizzards of snow and sharp ice around the valley. It's a good thing everyone packed warm clothes! To make it across safely, you'll need to find a way to avoid them.

Fortunately, it's easy to see all of this from the entrance to the valley, so you make a map of the valley and the blizzards (your puzzle input). For example:

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
The walls of the valley are drawn as #; everything else is ground. Clear ground - where there is currently no blizzard - is drawn as .. Otherwise, blizzards are drawn with an arrow indicating their direction of motion: up (^), down (v), left (<), or right (>).

The above map includes two blizzards, one moving right (>) and one moving down (v). In one minute, each blizzard moves one position in the direction it is pointing:

#.#####
#.....#
#.>...#
#.....#
#.....#
#...v.#
#####.#
Due to conservation of blizzard energy, as a blizzard reaches the wall of the valley, a new blizzard forms on the opposite side of the valley moving in the same direction. After another minute, the bottom downward-moving blizzard has been replaced with a new downward-moving blizzard at the top of the valley instead:

#.#####
#...v.#
#..>..#
#.....#
#.....#
#.....#
#####.#
Because blizzards are made of tiny snowflakes, they pass right through each other. After another minute, both blizzards temporarily occupy the same position, marked 2:

#.#####
#.....#
#...2.#
#.....#
#.....#
#.....#
#####.#
After another minute, the situation resolves itself, giving each blizzard back its personal space:

#.#####
#.....#
#....>#
#...v.#
#.....#
#.....#
#####.#
Finally, after yet another minute, the rightward-facing blizzard on the right is replaced with a new one on the left facing the same direction:

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
This process repeats at least as long as you are observing it, but probably forever.

Here is a more complex example:

#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
Your expedition begins in the only non-wall position in the top row and needs to reach the only non-wall position in the bottom row. On each minute, you can move up, down, left, or right, or you can wait in place. You and the blizzards act simultaneously, and you cannot share a position with a blizzard.

In the above example, the fastest way to reach your goal requires 18 steps. Drawing the position of the expedition as E, one way to achieve this is:

Initial state:
#E######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#

Minute 1, move down:
#.######
#E>3.<.#
#<..<<.#
#>2.22.#
#>v..^<#
######.#

Minute 2, move down:
#.######
#.2>2..#
#E^22^<#
#.>2.^>#
#.>..<.#
######.#

Minute 3, wait:
#.######
#<^<22.#
#E2<.2.#
#><2>..#
#..><..#
######.#

Minute 4, move up:
#.######
#E<..22#
#<<.<..#
#<2.>>.#
#.^22^.# 
######.#

Minute 5, move right:
#.######
#2Ev.<>#
#<.<..<#
#.^>^22#
#.2..2.#
######.#

Minute 6, move right:
#.######
#>2E<.<#
#.2v^2<#
#>..>2>#
#<....>#
######.#

Minute 7, move down:
#.######
#.22^2.#
#<vE<2.#
#>>v<>.#
#>....<#
######.#

Minute 8, move left:
#.######
#.<>2^.#
#.E<<.<#
#.22..>#
#.2v^2.#
######.#

Minute 9, move up:
#.######
#<E2>>.#
#.<<.<.#
#>2>2^.#
#.v><^.# 
######.#

Minute 10, move right:
#.######
#.2E.>2#
#<2v2^.#
#<>.>2.#
#..<>..#
######.#

Minute 11, wait:
#.######
#2^E^2>#
#<v<.^<#
#..2.>2#
#.<..>.#
######.#

Minute 12, move down:
#.######
#>>.<^<#
#.<E.<<#
#>v.><>#
#<^v^^>#
######.#

Minute 13, move down:
#.######
#.>3.<.#
#<..<<.#
#>2E22.#
#>v..^<#
######.#

Minute 14, move right:
#.######
#.2>2..#
#.^22^<#
#.>2E^>#
#.>..<.#
######.#

Minute 15, move right:
#.######
#<^<22.#
#.2<.2.#
#><2>E.#
#..><..#
######.#

Minute 16, move right:
#.######
#.<..22#
#<<.<..#
#<2.>>E#
#.^22^.# 
######.#

Minute 17, move down:
#.######
#2.v.<>#
#<.<..<#
#.^>^22#
#.2..2E#
######.#

Minute 18, move down:
#.######
#>2.<.<#
#.2v^2<#
#>..>2>#
#<....>#
######E#
What is the fewest number of minutes required to avoid the blizzards and reach the goal?

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
As the expedition reaches the far side of the valley, one of the Elves looks especially dismayed:

He forgot his snacks at the entrance to the valley!

Since you're so good at dodging blizzards, the Elves humbly request that you go back for his snacks. From the same initial conditions, how quickly can you make it from the start to the goal, then back to the start, then back to the goal?

In the above example, the first trip to the goal takes 18 minutes, the trip back to the start takes 23 minutes, and the trip back to the goal again takes 13 minutes, for a total time of 54 minutes.

What is the fewest number of minutes required to reach the goal, go back to the start, then reach the goal again?
"""

import sys
import os
from collections import deque

# Add the root directory to the Python path (for testing purposes)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from common.test_framework import run_tests

def parse_input(lines):
    """Parse the input lines and return the initial blizzards and valley dimensions."""
    walls = set()
    blizzards = {'<': [], '>': [], '^': [], 'v': []}
    
    height = len(lines)
    width = len(lines[0].strip())
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == '#':
                walls.add((x, y))
            elif char in '<>^v':
                blizzards[char].append((x, y))
    
    return walls, blizzards, height, width

def move_blizzards(blizzards, height, width):
    """Move all blizzards one step and return new positions."""
    new_blizzards = {'<': [], '>': [], '^': [], 'v': []}
    
    # Handle horizontal blizzards
    for x, y in blizzards['<']:
        # new_x = x - 1 if x > 1 else width - 2 # This is a short hand if statement
         # Check if the blizzard is at the left edge (x <= 1)
        if x > 1:
            # If not at the edge, move one step to the left
            new_x = x - 1
        else:
            # If at the edge, wrap around to the right side
            new_x = width - 2
        new_blizzards['<'].append((new_x, y))
    
    for x, y in blizzards['>']:
        # Check if the blizzard is at the right edge (x >= width - 2)
        if x < width - 2:
            # If not at the edge, move one step to the right
            new_x = x + 1
        else:
            # If at the edge, wrap around to the left side (position 1)
            new_x = 1
        new_blizzards['>'].append((new_x, y))
    
    # Handle vertical blizzards
    for x, y in blizzards['^']:
        # Check if the blizzard is at the top edge (y <= 1)
        if y > 1:
            # If not at the top edge, move one step up
            new_y = y - 1
        else:
            # If at the top edge, wrap around to the bottom (height - 2)
            new_y = height - 2
        new_blizzards['^'].append((x, new_y))
    
    for x, y in blizzards['v']:
        # Check if the blizzard is at the bottom edge (y >= height - 2)
        if y < height - 2:
            # If not at the bottom edge, move one step down
            new_y = y + 1
        else:
            # If at the bottom edge, wrap around to the top (position 1)
            new_y = 1
        new_blizzards['v'].append((x, new_y))
        
    return new_blizzards

def get_blizzard_positions(blizzards):
    """Get set of all positions occupied by blizzards."""
    positions = set()
    for direction in blizzards.values():
        positions.update(direction)
    return positions

def find_shortest_path_1(walls, blizzards, height, width, start, end):
    """Find shortest path from start to end avoiding blizzards."""
    queue = deque([(start, 0)])
    seen = {(start, 0)}
    
    # Cache blizzard positions for each minute
    blizzard_cache = {}
    
    while queue:
        pos, time = queue.popleft()
        
        if pos == end:
            return time
        
        # Get or calculate blizzard positions for next minute
        next_time = time + 1
        if next_time not in blizzard_cache:
            blizzards = move_blizzards(blizzards, height, width)
            blizzard_cache[next_time] = get_blizzard_positions(blizzards)
        blizzard_positions = blizzard_cache[next_time]
        
        # Try all possible moves including waiting
        x, y = pos
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (x + dx, y + dy)
            
            # Check if move is valid
            if (new_pos not in walls and 
                0 <= new_pos[0] < width and 
                0 <= new_pos[1] < height and 
                new_pos not in blizzard_positions and
                (new_pos, next_time) not in seen):
                    queue.append((new_pos, next_time))
                    seen.add((new_pos, next_time))
    
    return float('inf')


def blizzard_basin_1(lines):
    """Main function to solve the puzzle."""
    # Parse input
    walls, blizzards, height, width = parse_input(lines)
    
    # Find start and end positions
    start = (lines[0].index('.'), 0)
    end = (lines[-1].index('.'), len(lines) - 1)
    
    # Find shortest path
    time = find_shortest_path_1(walls, blizzards, height, width, start, end)
    return time

def find_shortest_path_2(walls, blizzards, height, width, start, end):
    """Find shortest path from start to end avoiding blizzards."""
    queue = deque([(start, 0)])
    seen = {(start, 0)}
    
    # Cache blizzard positions for each minute
    blizzard_cache = {}
    current_blizzards = blizzards.copy()  # Create a copy of initial blizzards
    
    while queue:
        pos, time = queue.popleft()
        
        if pos == end:
            return time, current_blizzards  # Return time taken for this specific journey
        
        # Get or calculate blizzard positions for next minute
        next_time = time + 1
        if next_time not in blizzard_cache:
            current_blizzards = move_blizzards(current_blizzards, height, width)
            blizzard_cache[next_time] = get_blizzard_positions(current_blizzards)
        blizzard_positions = blizzard_cache[next_time]
        
        # Try all possible moves including waiting
        x, y = pos
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (x + dx, y + dy)
            
            # Check if move is valid
            if (new_pos not in walls and 
                0 <= new_pos[0] < width and 
                0 <= new_pos[1] < height and 
                new_pos not in blizzard_positions and
                (new_pos, next_time) not in seen):
                    queue.append((new_pos, next_time))
                    seen.add((new_pos, next_time))
    
    return float('inf'), current_blizzards


def blizzard_basin_2(lines):
    """Main function to solve Part Two of the puzzle."""
    # Parse input
    walls, initial_blizzards, height, width = parse_input(lines)
    
    # Find start and end positions
    start = (lines[0].index('.'), 0)
    end = (lines[-1].index('.'), len(lines) - 1)
    
    # First journey: Start to Goal
    time_to_goal, blizzards_after_first = find_shortest_path_2(walls, initial_blizzards, height, width, start, end)
    
    # Move blizzards to their positions after first journey
    for _ in range(time_to_goal):
        initial_blizzards = move_blizzards(initial_blizzards, height, width)
    
    # Second journey: Goal to Start
    time_back_to_start, blizzards_after_second = find_shortest_path_2(walls, initial_blizzards, height, width, end, start)
    
    # Move blizzards to their positions after second journey
    for _ in range(time_back_to_start):
        initial_blizzards = move_blizzards(initial_blizzards, height, width)
    
    # Third journey: Start to Goal again
    time_back_to_goal, _ = find_shortest_path_2(walls, initial_blizzards, height, width, start, end)
    
    # Return sum of all three journey times
    return time_to_goal + time_back_to_start + time_back_to_goal

def test_solution():
    """Test the solution with the example input."""
    test_input = [
        "#.######",
        "#>>.<^<#",
        "#.<..<<#",
        "#>v.><>#",
        "#<^v^^>#",
        "######.#"
    ]
    
    test_cases = [
        (blizzard_basin_1, [test_input], 18, "Example test case - fewest number of minutes to reach the goal"),
        (blizzard_basin_2, [test_input], 54, "Example test case - fewest number of minutes to reach the goal, return to start, and reach the goal again"),
    ]
    
    run_tests(test_cases)
    result = solve_from_file("input.txt", part=1)
    print(f"Solution Part 1: Fewest number of minutes to reach the goal: {result}")
    result = solve_from_file("input.txt", part=2)
    print(f"Solution Part 2: Fewest number of minutes to reach the goal, return to start, and reach the goal again: {result}")

def solve_from_file(file_path, part=1):
    """Read input from file and solve the puzzle."""
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    full_file_path = os.path.join(script_dir, file_path)
    
    with open(full_file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        
    if part == 1:
        return blizzard_basin_1(lines)
    else:
        return blizzard_basin_2(lines)

if __name__ == "__main__":
    # Run test with example input
    test_solution()
    
    