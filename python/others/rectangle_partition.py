"""
################################################################################
#                           Rectangle Partition Problem                        #
################################################################################
# Source: https://www.codingame.com/ide/puzzle/rectangle-partition             #
################################################################################

Goal:
-----
There is a rectangle of given width w and height h.
On the width side, you are given a list of measurements.
On the height side, you are given another list of measurements.
Draw perpendicular lines from the measurements to partition the rectangle into
smaller rectangles. In all sub-rectangles (including the combinations of smaller
rectangles), how many of them are squares?

Input Format:
------------
Line 1: Integers w h countX countY (separated by space)
Line 2: list of measurements on the width side, countX integers separated by space,
       sorted in ascending order
Line 3: list of measurements on the height side, countY integers separated by space,
       sorted in ascending order

Output Format:
-------------
Line 1: the number of squares in sub-rectangles created by the added lines

Constraints:
-----------
* 1 ≤ w, h ≤ 20,000
* 1 ≤ number of measurements on each axis ≤ 500

Example:
--------
Input:
    10 5 2 1
    2 5
    3

Visual Representation:
    ___2______5__________
   |   |      |          |
   |   |      |          |
  3|___|______|__________|
   |   |      |          |
   |___|______|__________|

Output:
    4 (one 2x2, one 3x3, two 5x5 squares)

Note:
-----
The width and height measurements provided create a grid of intersection points.
The goal is to count all possible squares that can be formed using these points
as corners, including squares that span multiple smaller rectangles.

################################################################################
#                              Solution Methods                                  #
################################################################################

Solution Approaches Overview:
---------------------------
We implement two different approaches to solve this problem:
1. Direct Solution: A straightforward, brute-force approach
2. Optimized Solution: An improved version using length counting and early pruning

Key Differences:
- Solution 1 checks every possible rectangle combination
- Solution 2 optimizes by pre-processing lengths and using efficient data structures

The core functions take (w, h, x_measurements, y_measurements) directly so they
are unit-testable; ``solve_from_stdin()`` keeps the original CodinGame I/O.
"""

from common.test_framework import run_tests

################################################################################
#                           Solution 1: Direct Approach                        #
################################################################################
"""
Direct Solution Explanation:
--------------------------
This solution uses a straightforward approach:

1. Data Preparation:
   - Add 0 as starting point for both axes
   - Include all measurements
   - Add width/height as end points

2. Algorithm Process:
   - Uses nested loops to check all possible rectangle combinations
   - For each combination of points, checks if they form a square

3. Time Complexity: O(n²m²)
   - n: number of x-axis points
   - m: number of y-axis points

4. Advantages:
   - Simple to understand and implement
   - Good for small inputs

5. Disadvantages:
   - Slower for large inputs
   - Checks many invalid combinations
"""

def direct_count(w, h, x_measurements, y_measurements):
    # Build the point lists including 0 and the width/height boundaries.
    X_pts = [0] + list(x_measurements) + [w]
    Y_pts = [0] + list(y_measurements) + [h]

    count = 0
    lenX_pts = len(X_pts)
    lenY_pts = len(Y_pts)

    # Check all possible rectangles formed by the points.
    for i in range(lenX_pts - 1):
        for j in range(i + 1, lenX_pts):
            for k in range(lenY_pts - 1):
                for l in range(k + 1, lenY_pts):
                    x1, y1 = X_pts[i], Y_pts[k]
                    x2, y2 = X_pts[j], Y_pts[l]

                    # Check if it's a valid square.
                    if x2 > x1 and y2 > y1 and (x2 - x1 == y2 - y1):
                        count += 1

    return count

################################################################################
#                        Solution 2: Optimized Approach                        #
################################################################################
"""
Optimized Solution Explanation:
----------------------------
This solution improves performance through several optimization techniques:

1. Key Optimizations:
   a) Length Pre-processing:
      - Calculate all possible lengths on x-axis
      - Only store lengths that could form valid squares
      - Track frequency of each length on both axes

   b) Early Pruning:
      - Skip lengths larger than min(w,h)
      - Break loops early when exceeding boundaries
      - Only process lengths that exist in both axes

2. Time Complexity: O(n²m) in practice
   - Early pruning reduces actual computations

3. Space Complexity: O(n + m)

Key trick: the number of squares of a given side length equals
(count of that length on the x-axis) * (count of that length on the y-axis),
summed over all lengths.
"""


def count_squares(w, h, x_measurements, y_measurements):
    # Add boundary points and sort.
    x_points = sorted([0, w] + list(x_measurements))
    y_points = sorted([0, h] + list(y_measurements))

    # Store all lengths with their [x_count, y_count] frequencies.
    length_counts = {}

    # Process x-axis lengths.
    for i in range(len(x_points)):
        for j in range(i + 1, len(x_points)):
            length = x_points[j] - x_points[i]
            if length > min(w, h):  # Early pruning
                break
            length_counts[length] = length_counts.get(length, [0, 0])
            length_counts[length][0] += 1

    # Process y-axis lengths.
    for i in range(len(y_points)):
        for j in range(i + 1, len(y_points)):
            length = y_points[j] - y_points[i]
            if length > min(w, h):  # Early pruning
                break
            if length in length_counts:  # Only store if it exists on the x-axis
                length_counts[length][1] += 1

    return sum(x_count * y_count for x_count, y_count in length_counts.values())


def solve_from_stdin():
    """Original CodinGame I/O: read w h countX countY, then the two rows."""
    w, h, _count_x, _count_y = map(int, input().split())
    x_measurements = list(map(int, input().split()))
    y_measurements = list(map(int, input().split()))
    return count_squares(w, h, x_measurements, y_measurements)


################################################################################
#                                   Tests                                      #
################################################################################
def test_solution():
    # Both approaches must agree with the documented results.
    test_cases = [
        (count_squares, [10, 5, [2, 5], [3]], 4, "Optimized: docstring example"),
        (count_squares, [2, 2, [], []], 1, "Optimized: single 2x2 square"),
        (count_squares, [4, 4, [2], [2]], 5, "Optimized: 3x3 grid (4x 2x2 + 1x 4x4)"),
        (direct_count, [10, 5, [2, 5], [3]], 4, "Direct: docstring example"),
        (direct_count, [2, 2, [], []], 1, "Direct: single 2x2 square"),
        (direct_count, [4, 4, [2], [2]], 5, "Direct: 3x3 grid (4x 2x2 + 1x 4x4)"),
    ]

    run_tests(test_cases)


if __name__ == "__main__":
    # Self-test by default. For real CodinGame input, call solve_from_stdin().
    test_solution()
