import sys
import os
import pytest

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import all test modules
import codewars.luck_check
import leetcode.easy.fizz_buzz
import leetcode.easy.is_subsequence
import leetcode.easy.majority_element
import leetcode.medium.three_sum
import leetcode.medium.two_sum_ii
import leetcode.medium.two_sum_ii

if __name__ == "__main__":
    # Run all tests and generate an HTML report
    pytest.main(["-q", "--tb=short", "--html=report.html", "--self-contained-html"])
