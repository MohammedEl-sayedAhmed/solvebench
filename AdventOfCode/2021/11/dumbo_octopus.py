"""
Advent of Code - Day 11: Dumbo Octopus
https://adventofcode.com/2021/day/11

You enter a large cavern full of rare bioluminescent dumbo octopuses! They seem to not like the Christmas lights on your submarine, so you turn them off for now.

There are 100 octopuses arranged neatly in a 10 by 10 grid. Each octopus slowly gains energy over time and flashes brightly for a moment when its energy is full. Although your lights are off, maybe you could navigate through the cave without disturbing the octopuses if you could predict when the flashes of light will happen.

Each octopus has an energy level - your submarine can remotely measure the energy level of each octopus (your puzzle input). For example:

5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526

The energy level of each octopus is a value between 0 and 9. Here, the top-left octopus has an energy level of 5, the bottom-right one has an energy level of 6, and so on.

You can model the energy levels and flashes of light in steps. During a single step, the following occurs:

First, the energy level of each octopus increases by 1.
Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once per step.)
Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.

Adjacent flashes can cause an octopus to flash on a step even if it begins that step with very little energy. Consider the middle octopus with 1 energy in this situation:

Before any steps:
11111
19991
19191
19991
11111

After step 1:
34543
40004
50005
40004
34543

After step 2:
45654
51115
61116
51115
45654

An octopus is highlighted when it flashed during the given step.

Here is how the larger example above progresses:

Before any steps:
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526

After step 1:
6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637

After step 2:
8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848

After step 3:
0050900866
8500800575
9900000039
9700000041
9935080063
7712300000
7911250009
2211130000
0421125000
0021119000

After step 4:
2263031977
0923031697
0032221150
0041111163
0076191174
0053411122
0042361120
5532241122
1532247211
1132230211

After step 5:
4484144000
2044144000
2253333493
1152333274
1187303285
1164633233
1153472231
6643352233
2643358322
2243341322

After step 6:
5595255111
3155255222
3364444605
2263444496
2298414396
2275744344
2264583342
7754463344
3754469433
3354452433

After step 7:
6707366222
4377366333
4475555827
3496655709
3500625609
3509955566
3486694453
8865585555
4865580644
4465574644

After step 8:
7818477333
5488477444
5697666949
4608766830
4734946730
4740097688
6900007564
0000009666
8000004755
6800007755

After step 9:
9060000644
7800000976
6900000080
5840000082
5858000093
6962400000
8021250009
2221130009
9111128097
7911119976

After step 10:
0481112976
0031112009
0041112504
0081111406
0099111306
0093511233
0442361130
5532252350
0532250600
0032240000

After step 10, there have been a total of 204 flashes. Fast forwarding, here is the same configuration every 10 steps:

After step 20:
3936556452
5686556806
4496555690
4448655580
4456865570
5680086577
7000009896
0000000344
6000000364
4600009543

After step 30:
0643334118
4253334611
3374333458
2225333337
2229333338
2276733333
2754574565
5544458511
9444447111
7944446119

After step 40:
6211111981
0421111119
0042111115
0003111115
0003111116
0065611111
0532351111
3322234597
2222222976
2222222762

After step 50:
9655556447
4865556805
4486555690
4458655580
4574865570
5700086566
6000009887
8000000533
6800000633
5680000538

After step 60:
2533334200
2743334640
2264333458
2225333337
2225333338
2287833333
3854573455
1854458611
1175447111
1115446111

After step 70:
8211111164
0421111166
0042111114
0004211115
0000211116
0065611111
0532351111
7322235117
5722223475
4572222754

After step 80:
1755555697
5965555609
4486555680
4458655580
4570865570
5700086566
7000008666
0000000990
0000000800
0000000000

After step 90:
7433333522
2643333522
2264333458
2226433337
2222433338
2287833333
2854573333
4854458333
3387779333
3333333333

After step 100:
0397666866
0749766918
0053976933
0004297822
0004229892
0053222877
0532222966
9322228966
7922286866
6789998766

After 100 steps, there have been a total of 1656 flashes.

Given the starting energy levels of the dumbo octopuses in your cavern, simulate 100 steps. How many total flashes are there after 100 steps?

--- Part Two ---
It seems like the individual flashes aren't bright enough to navigate. However, you might have a better option: the flashes seem to be synchronizing!

In the example above, the first time all octopuses flash simultaneously is step 195:
If you can calculate the exact moments when the octopuses will all flash simultaneously, you should be able to navigate through the cavern. What is the first step during which all octopuses flash?
"""

import sys
import os

# Add the root directory to the Python path (for testing purposes)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from common.test_framework import run_tests

def simulate_octopus_flashes_1(grid, steps):
    """
    Simulate the flashes of dumbo octopuses over a given number of steps.
    Each octopus gains energy and flashes when its energy exceeds 9,
    affecting adjacent octopuses.

    Args:
        grid (list of list of int): The initial energy levels of the octopuses
        steps (int): The number of steps to simulate

    Returns:
        int: The total number of flashes after the given number of steps
    """
    total_flashes = 0
    rows = len(grid)
    cols = len(grid[0])
    
    directions = [(-1,  1), (0,  1), (1,  1),
                  (-1,  0),          (1,  0),
                  (-1, -1), (0, -1), (1, -1)]
    
    def increase_energy(r, c, flashed):
        """
        Recursively handle the flash of a single octopus and its effects on neighbors.
        """
        
        valid_r = 0 <= r < rows
        valid_c = 0 <= c < cols
        valid_r_c = valid_r and valid_c
        
        # Return Condition 
        if (((r,c) in flashed) or 
            (not valid_r_c)):
            return 
        
        grid[r][c] += 1
        
        if grid[r][c] > 9:
            flashed.add((r,c))
            grid[r][c] = 0
            
            # Increase the energy for adjacent octopuses
            for dr, dc in directions:
                increase_energy(r + dr, c + dc, flashed)
        

    for i in range(steps):
        flashed = set()
        
        # First, increase energy of all octopuses by 1
        for r in range(rows):
            for c in range(cols):
                if (r,c) not in flashed:
                    increase_energy(r, c, flashed)
        
        total_flashes += len(flashed)
    
    return total_flashes

def simulate_octopus_flashes_2(grid):
    """
    Simulate the flashes of dumbo octopuses over a given number of steps.
    Each octopus gains energy and flashes when its energy exceeds 9,
    affecting adjacent octopuses.

    Args:
        grid (list of list of int): The initial energy levels of the octopuses
        steps (int): The number of steps to simulate

    Returns:
        int: The total number of flashes after the given number of steps
    """
    total_flashes = 0
    rows = len(grid)
    cols = len(grid[0])
        
    directions = [(-1,  1), (0,  1), (1,  1),
                  (-1,  0),          (1,  0),
                  (-1, -1), (0, -1), (1, -1)]
    
    def increase_energy(r, c, flashed):
        """
        Recursively handle the flash of a single octopus and its effects on neighbors.
        """
        
        valid_r = 0 <= r < rows
        valid_c = 0 <= c < cols
        valid_r_c = valid_r and valid_c
        
        # Return Condition 
        if (((r,c) in flashed) or 
            (not valid_r_c)):
            return 
        
        grid[r][c] += 1
        
        if grid[r][c] > 9:
            flashed.add((r,c))
            grid[r][c] = 0
            
            # Increase the energy for adjacent octopuses
            for dr, dc in directions:
                increase_energy(r + dr, c + dc, flashed)
        
    sync_step = 0
    while(1):
        sync_step += 1
        flashed = set()
        
        # First, increase energy of all octopuses by 1
        for r in range(rows):
            for c in range(cols):
                if (r,c) not in flashed:
                    increase_energy(r, c, flashed)
        
        total_flashes += len(flashed)
        if len(flashed) == rows * cols:
            return sync_step


def solve_from_file(file_path):
    """
    Reads the input grid from a file and returns it as a 2D list of integers.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    full_file_path = os.path.join(script_dir, file_path)
    
    with open(full_file_path, 'r') as file:
        grid = []
        for line in file:
            lineList = []
            line = line.strip()
            for char in line:
                lineList.append(int(char))
            grid.append(lineList)
    
    return grid
        
def test_solution():
    # Example test case from the problem description
    test_grid = [
        [
        [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
        [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
        [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
        [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
        [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
        [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
        [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
        [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
        [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
        [5, 2, 8, 3, 7, 5, 1, 5, 2, 6]
        ],
        [
        [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
        [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
        [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
        [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
        [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
        [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
        [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
        [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
        [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
        [5, 2, 8, 3, 7, 5, 1, 5, 2, 6]
        ],
        
        ]
    
    # Run test cases
    test_cases = [
        (simulate_octopus_flashes_1, [test_grid[0], 100], 1656, "Example test case - 100 steps"),
        (simulate_octopus_flashes_2, [test_grid[1]], 195, "Example test case - Synced flashes"),
    ]
    
    run_tests(test_cases)
    
    # Uncomment to run with actual input file
    grid = solve_from_file("input.txt")
    result_1 = simulate_octopus_flashes_1(grid, 100)
    print(f"Solution part 1: Total flashes after 100 steps: {result_1}")
    
    # Read the input again as it was modified from the run of previous function
    grid = solve_from_file("input.txt")
    result_2 = simulate_octopus_flashes_2(grid)
    print(f"Solution part 2: Synced flashes where all octopuses flash is : {result_2}")

if __name__ == "__main__":
    test_solution()