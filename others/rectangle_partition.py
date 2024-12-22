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
"""

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
   - Stores all valid points for potential future use

3. Time Complexity: O(n²m²)
   - n: number of x-axis points
   - m: number of y-axis points
   
4. Advantages:
   - Simple to understand and implement
   - Good for small inputs
   - Maintains list of all valid points

5. Disadvantages:
   - Slower for large inputs
   - Checks many invalid combinations
"""

def direct_solution():
    # Read the input
    w, h, count_x, count_y = [int(i) for i in input().split()]

    # Initialize arrays for x and y with a 0 at the beginning
    X_pts = [0]
    Y_pts = [0]

    # Read the x-axis measurements and add them to X_pts
    x_measurements = [int(i) for i in input().split()]
    X_pts.extend(x_measurements)
    X_pts.append(w)

    # Read the y-axis measurements and add them to Y_pts
    y_measurements = [int(i) for i in input().split()]
    Y_pts.extend(y_measurements)
    Y_pts.append(h)

    count = 0
    lenX_pts = len(X_pts)
    lenY_pts = len(Y_pts)
    valid_pts = []

    # Check all possible rectangles formed by the points
    for i in range(lenX_pts - 1):
        for j in range(i+1, lenX_pts):
            for k in range(lenY_pts - 1):
                for l in range(k+1, lenY_pts):
                    valid_pts.append((X_pts[i], Y_pts[k], X_pts[j], Y_pts[l]))
                    
                    # Get coordinates of the sub-rectangle
                    x1, y1 = X_pts[i], Y_pts[k]
                    x2, y2 = X_pts[j], Y_pts[l]
                    
                    # Check if it's a valid square
                    if x2 > x1 and y2 > y1:
                        if (x2 - x1 == y2 - y1):
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
   
   c) Efficient Data Structures:
      - Use sets for O(1) point lookup
      - Dictionary to store length frequencies
      - Sorted points for sequential access

2. Algorithm Steps:
   a) Prepare Data:
      - Create sorted point lists with boundaries
      - Convert to sets for fast lookup
   
   b) Process Lengths:
      - Calculate all x-axis lengths and frequencies
      - Match with y-axis lengths
      - Store only valid candidates
   
   c) Count Squares:
      - Check only valid lengths
      - Verify corner points exist
      - Count valid square formations

3. Time Complexity: O(n²m) in practice
   - Significantly faster than direct approach
   - Early pruning reduces actual computations

4. Space Complexity: O(n + m)
   - Additional space for sets and length counts
   - Trade-off for better time complexity
"""


def optimized_solution():
    def count_squares(w, h, x_measurements, y_measurements):
        # Add boundary points and sort
        x_points = sorted([0, w] + x_measurements)
        y_points = sorted([0, h] + y_measurements)
        
        # Create sets for O(1) lookup
        x_set = set(x_points)
        y_set = set(y_points)
        
        # Store all lengths with their frequencies
        length_counts = {}
        
        # Process x-axis lengths
        for i in range(len(x_points)):
            for j in range(i + 1, len(x_points)):
                length = x_points[j] - x_points[i]
                if length > min(w, h):  # Early pruning
                    break
                length_counts[length] = length_counts.get(length, [0, 0])
                length_counts[length][0] += 1
        
        # Process y-axis lengths
        for i in range(len(y_points)):
            for j in range(i + 1, len(y_points)):
                length = y_points[j] - y_points[i]
                if length > min(w, h):  # Early pruning
                    break
                if length in length_counts:  # Only store if exists in x-axis
                    length_counts[length][1] += 1
        
        resultDict = sum(value[0] * value[1] for value in length_counts.values())
        return resultDict
        """
        If we don't get the trick where summation of value[0] * value[1] is the total sum, we can do the following
        square_count = 0
        # Check all possible squares
        for length, (x_count, y_count) in length_counts.items():
            if y_count == 0:  # Skip if length doesn't exist in y-axis
                continue
                
            for x in x_points:
                if x + length > w: # can be removed if we are sure that the lists are sorted
                    continue
                if x + length not in x_set:
                    continue
                    
                for y in y_points:
                    if y + length > h: # can be removed if we are sure that the lists are sorted
                        break
                    if y + length in y_set:
                        square_count += 1
        
        return square_count
        """

    # Read input
    w, h, count_x, count_y = map(int, input().split())
    x_measurements = list(map(int, input().split()))
    y_measurements = list(map(int, input().split()))
    return count_squares(w, h, x_measurements, y_measurements)

################################################################################
#                               Main Execution                                 #
################################################################################
"""
Usage Notes:
-----------
1. For small inputs (few measurements), both solutions work well
2. For large inputs, optimized solution (Solution 2) is recommended
3. Uncomment the desired solution in the main block below
"""

if __name__ == "__main__":
    # Choose which solution to run
    # result = direct_solution()    # Solution 1
    result = optimized_solution()   # Solution 2
    print(result)