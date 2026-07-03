class TestFailure(AssertionError):
    """Raised when one or more test cases fail, so runners exit non-zero."""


def run_tests(test_cases):
    """
    Run the provided test cases, print the results, and FAIL LOUDLY on any miss.

    Prints a ✅/❌ line per case and a summary, then raises ``TestFailure`` if any
    case failed. Raising (rather than only printing) is what lets ``run.py`` and
    ``pytest`` detect failures via a non-zero exit / failed assertion.

    :param test_cases: A list of tuples ``(function, args, expected, test_name)``.
    """
    passed = 0
    total = len(test_cases)
    failures = []

    for func, args, expected, name in test_cases:
        result = func(*args)
        if result == expected:
            passed += 1
            print(f"✅  {name}")
        else:
            failures.append(name)
            print(f"❌  {name}")
            print(f"      expected: {expected}")
            print(f"      got:      {result}")

    print("\n" + "─" * 34)
    if not failures:
        print(f"🎉  {passed}/{total} passed — all green")
    else:
        print(f"❌  {passed}/{total} passed · {len(failures)} failed")
        raise TestFailure(f"{len(failures)}/{total} failed: {', '.join(failures)}")
