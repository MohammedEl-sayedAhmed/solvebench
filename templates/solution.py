"""
<Problem Title>
<url>

<problem statement — paste here>
"""

from common.test_framework import run_tests


class Solution:
    def solve(self, *args):
        """Explain the approach. Time O(?), Space O(?)."""
        raise NotImplementedError


def test_solution():
    solution = Solution()

    test_cases = [
        # (solution.solve, [args], expected, "Example 1"),
    ]

    run_tests(test_cases)


if __name__ == "__main__":
    test_solution()
