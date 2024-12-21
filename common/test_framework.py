def run_tests(test_cases):
    """
    Run the provided test cases and print the results.
    
    :param test_cases: A list of tuples containing (function, input args, expected output, test name)
    """
    passed_tests = 0
    total_tests = len(test_cases)

    for case in test_cases:
        func, args, expected, test_name = case  # Unpack the case
        result = func(*args)  # Call the function with the provided arguments
        if result == expected:
            passed_tests += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
            print(f"   Input: {args}")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")

    # Print metrics
    print(f"\nTest Results: {passed_tests}/{total_tests} passed")
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
