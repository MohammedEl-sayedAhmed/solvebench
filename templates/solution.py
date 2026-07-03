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


# Optional: custom input scaling for `./run.sh complexity <problem>` — only
# needed when the input can't be derived from the type hints.
# def complexity_input(n):
#     return [list(range(n))]   # the argument list for input size n


def test_solution():
    solution = Solution()

    test_cases = [
        # (solution.solve, [args], expected, "Example 1"),
    ]

    run_tests(test_cases)


if __name__ == "__main__":
    test_solution()
