"""
Advent of Code - Day 14: Regolith Reservoir
https://adventofcode.com/2022/day/14

The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:

  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?

--- Part Two ---
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
"""

from common.aoc import input_path

from common.test_framework import run_tests

def parse_input(lines):
    """
    Parse the input lines and return the cave grid and sand source.
    """
    paths = []
    for line in lines:
        path = []
        points = line.strip().split(' -> ')
        for point in points:
            (x, y)  = (tuple(map(int, point.split(','))))
            path.append((x, y))
        paths.append(path)
    
    return paths

def create_grid(paths):
    """
    Create a grid based on the paths of rock structures.
    """
    # Grid for simulating the coordinates of the rocks
    grid = set()
    max_y = float('-inf')  # Initialize max_y with a very small number
    
    # Draw the grid of the rocks, horizontal and vertical lines
    for path in paths:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            
            # Update max_y to track the highest y value
            max_y = max(max_y, y1, y2)

            # Generate vertical line (for same x, different y), if x1 == x2
            if x1 == x2:
                min_y_point = min(y1, y2)
                max_y_point = max(y1, y2)
                for y in range(min_y_point, max_y_point + 1):
                    grid.add((x1, y)) # Add vertical line to the grid
            # Generate horizontal line (for same y, different x)        
            else:
                min_x_point = min(x1, x2)
                max_x_point = max(x1, x2)
                for x in range(min_x_point, max_x_point + 1):
                    grid.add((x, y1)) # Add horizontal line to the grid
    
    return grid, max_y
                
def simulate_sand_1(grid, max_y, source=(500, 0)):
    """
    Simulate falling sand and return the number of sand units that come to rest.
    Using a set-based approach for better performance.
    """
    sand_count = 0
    # the sand is here at
    #                     (0,  0)
    directions = [(0, 1), (-1, 1), (1, 1)]  # Down, down-left, down-right
    
    while True:
        x, y = source
        
        while True:
            if y >= max_y: # Sand has reached the abyss
                return sand_count
            
            moved = False
            for dx, dy in directions:
                sand_location_prime = (x + dx, y + dy)
                if sand_location_prime not in grid: # this location is not a rock, can be moved
                    x += dx
                    y += dy
                    moved = True
                    break
            
            # This means that it was blocked with a rock, another sand, etc    
            if not moved:
                grid.add((x, y))
                sand_count += 1
                break

def simulate_sand_2(grid, max_y, source=(500, 0)):
    """
    Simulate falling sand and return the number of sand units that come to rest.
    Using a set-based approach for better performance.
    """
    sand_count = 0
    # the sand is here at
    #                     (0,  0)
    directions = [(0, 1), (-1, 1), (1, 1)]  # Down, down-left, down-right
    
    while True:
        x, y = source
        
        while True:
            if y >= max_y + 2: # Reaches the floor
                grid.add((x, y)) 
                # No need to increment the sand count as it was already incremented when it was coming to rest
                break
            
            moved = False
            for dx, dy in directions:
                sand_location_prime = (x + dx, y + dy)
                if sand_location_prime not in grid: # this location is not a rock, can be moved
                    x += dx
                    y += dy
                    moved = True
                    break
            
            # This means that it was blocked with a rock, another sand, etc    
            if not moved:
                grid.add((x, y))
                sand_count += 1
                if (x, y) == source:
                    return sand_count
                break

def regolith_reservoir_1(lines):
    """
    Main function to solve the puzzle.
    """
    paths = parse_input(lines)
    grid, max_y = create_grid(paths)
    return simulate_sand_1(grid, max_y)

def regolith_reservoir_2(lines):
    """
    Main function to solve the puzzle.
    """
    paths = parse_input(lines)
    grid, max_y = create_grid(paths)
    return simulate_sand_2(grid, max_y)

def solve_from_file(file_path, part=1):
    """
    Reads the input lines from a file and returns the result of the puzzle.
    """
    full_file_path = input_path(__file__, file_path)
    
    with open(full_file_path, 'r') as file:
        lines = file.readlines()
    
    if part == 1:
        return regolith_reservoir_1(lines)
    else:
        return regolith_reservoir_2(lines)

def test_solution():
    """
    Test the solution with the example input.
    """
    test_input = [
        "498,4 -> 498,6 -> 496,6",
        "503,4 -> 502,4 -> 502,9 -> 494,9"
    ]
    
    test_cases = [
        (regolith_reservoir_1, [test_input], 24, "Example test case - units of sand that come to rest, at abyss"),
        (regolith_reservoir_2, [test_input], 93, "Example test case - units of sand that come to rest, at floor"),
    ]
    
    run_tests(test_cases)
    
    # Uncomment to run with actual input file
    result = solve_from_file("input.txt", part=1)
    print(f"Solution Part 1: Units of sand that come to rest: {result}")
    result = solve_from_file("input.txt", part=2)
    print(f"Solution Part 2: Units of sand that come to rest: {result}")

if __name__ == "__main__":
    test_solution()
