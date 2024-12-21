"""
Count IP Addresses
https://www.codewars.com/kata/count-ip-addresses

Implement a function that receives two IPv4 addresses, and returns the number of addresses between them (including the first one, excluding the last one).

All inputs will be valid IPv4 addresses in the form of strings. The last address will always be greater than the first one.

Examples:
* With input "10.0.0.0", "10.0.0.50"  => return   50 
* With input "10.0.0.0", "10.0.1.0"   => return  256 
* With input "20.0.0.10", "20.0.1.0"  => return  246
"""

def ips_between(start, end):
    # convert ip to int [use reverse in loop]
    # startList = start.split('.')
    # endList = end.split('.')
    # startSum = 0
    # endSum = 0
    # for i, ip in enumerate(reversed(startList)):
    #     startSum += int(ip) * (256**i)
    # for i, ip in enumerate(reversed(endList)):
    #     endSum += int(ip) * (256**i)
    # return endSum - startSum 
    
    # Use the information that the ip will always be 4 parts, i = [0,3]
    # startList = start.split('.')
    # endList = end.split('.')
    # startSum = 0
    # endSum = 0
    # i_vals = [3, 2, 1, 0]
    # for i, ip in enumerate(startList):
    #     startSum += int(ip) * (256**i_vals[i])
    # for i, ip in enumerate(endList):
    #     endSum += int(ip) * (256**i_vals[i])
    # return endSum - startSum 

    
    # More Neat solution
    # Convert IP addresses to integer
    def ip_to_int(ip: str) -> int:
       parts = list(map(int, ip.split('.')))
       return parts[0] * 256**3 + parts[1] * 256**2 + parts[2] * 256 + parts[3]
    start_int = ip_to_int(start)
    end_int = ip_to_int(end)
    # Return the difference between the two addresses
    return end_int - start_int


    
    

def test_solution():
    """
    Test function with various test cases to verify the solution.
    """
    test_cases = [
        ("10.0.0.0", "10.0.0.50", 50, "Test Case 1"),
        ("10.0.0.0", "10.0.1.0", 256, "Test Case 2"),
        ("20.0.0.10", "20.0.1.0", 246, "Test Case 3"),
        ("192.168.1.1", "192.168.1.10", 9, "Test Case 4"),
        ("0.0.0.0", "0.0.0.1", 1, "Test Case 5"),
        ("255.255.255.255", "255.255.255.255", 0, "Test Case 6"),  # Edge case, same IP
    ]
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for start, end, expected, test_name in test_cases:
        result = ips_between(start, end)
        if result == expected:
            passed_tests += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
            print(f"   Input: start = \"{start}\", end = \"{end}\"")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")

    # Print metrics
    print(f"\nTest Results: {passed_tests}/{total_tests} passed")
    if passed_tests == total_tests:
        print("All tests passed! 🎉")

if __name__ == "__main__":
    test_solution() 