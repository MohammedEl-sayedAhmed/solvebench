"""
888. Fair Candy Swap
https://leetcode.com/problems/fair-candy-swap/

Alice and Bob have a different total number of candies. You are given two integer arrays aliceSizes and bobSizes where aliceSizes[i] is the number of candies of the ith box of candy that Alice has and bobSizes[j] is the number of candies of the jth box of candy that Bob has.

Since they are friends, they would like to exchange one candy box each so that after the exchange, they both have the same total amount of candy. The total amount of candy a person has is the sum of the number of candies in each box they have.

Return an integer array answer where answer[0] is the number of candies in the box that Alice must exchange, and answer[1] is the number of candies in the box that Bob must exchange. If there are multiple answers, you may return any one of them. It is guaranteed that at least one answer exists.

Example 1:
Input: aliceSizes = [1,1], bobSizes = [2,2]
Output: [1,2]

Example 2:
Input: aliceSizes = [1,2], bobSizes = [2,3]
Output: [1,2]

Example 3:
Input: aliceSizes = [2], bobSizes = [1,3]
Output: [2,3]

Constraints:
1 <= aliceSizes.length, bobSizes.length <= 10^4
1 <= aliceSizes[i], bobSizes[j] <= 10^5
Alice and Bob have a different total number of candies.
There will be at least one valid answer for the given input.
"""

class Solution:
    def fairCandySwap(self, aliceSizes: list[int], bobSizes: list[int]) -> list[int]:
        
        # Solution 1: Brute force
        # alice_sum = sum(aliceSizes)
        # bob_sum = sum(bobSizes)
        
        # total = alice_sum + bob_sum
        # each_sum = total // 2
        # result = []
        
        # for i in aliceSizes:
        #     for j in bobSizes:
        #         x = each_sum - alice_sum
        #         if x == (j - i):
        #             result = [i, j]
        #             return result
        
        
        # Solution 2 using sets to be O(n + m)
        alice_sum = sum(aliceSizes)
        bob_sum = sum(bobSizes)
        
        total = alice_sum + bob_sum
        each_sum = total // 2
        result = []
        setB = set(bobSizes)
        
        for i in aliceSizes:
            x = each_sum - alice_sum + i
            if x in setB:
                result = [i, x]
                break
        return result
            
        
        

            
            
        

                    
        


def test_solution():
    solution = Solution()
    
    test_cases = [
        ([1, 1], [2, 2], [1, 2], "Example 1"),
        ([1, 2], [2, 3], [1, 2], "Example 2"),
        ([2], [1, 3], [2, 3], "Example 3"),
        ([1, 3, 5], [2, 4, 6], [1, 2], "Additional Test 1")
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for aliceSizes, bobSizes, expected, test_name in test_cases:
        result = solution.fairCandySwap(aliceSizes, bobSizes)
        if result == expected:
            print(f"✅ {test_name} passed")
            passed_tests += 1
        else:
            print(f"\n❌ {test_name} failed")
            print(f"   Input: aliceSizes = {aliceSizes}, bobSizes = {bobSizes}")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")
    
    print(f"\nTest Results: {passed_tests}/{total_tests} passed")
    if passed_tests == total_tests:
        print("All tests passed! 🎉")
    else:
        print(f"Failed {total_tests - passed_tests} tests")


if __name__ == "__main__":
    test_solution() 