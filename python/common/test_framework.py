class TestFailure(AssertionError):
    """Raised when one or more test cases fail, so runners exit non-zero."""


def run_tests(test_cases):
    """
    Run the provided test cases, print the results, and FAIL LOUDLY on any miss.

    Prints a ✅/❌ line per case and a summary, then raises ``TestFailure`` if any
    case failed. Raising (rather than only printing) is what lets ``run.py`` and
    ``pytest`` detect failures via a non-zero exit / failed assertion — previously
    a wrong answer still reported as "passed".

    :param test_cases: A list of tuples ``(function, args, expected, test_name)``.
    """
    passed_tests = 0
    total_tests = len(test_cases)
    failures = []

    for func, args, expected, test_name in test_cases:
        result = func(*args)  # Call the function with the provided arguments
        if result == expected:
            passed_tests += 1
            print(f"✅ {test_name} passed")
        else:
            failures.append(test_name)
            print(f"❌ {test_name} failed")
            print(f"   Input: {args}")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")

    # Print metrics
    print(f"\nTest Results: {passed_tests}/{total_tests} passed")
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
    else:
        raise TestFailure(
            f"{len(failures)}/{total_tests} test(s) failed: {', '.join(failures)}"
        )
