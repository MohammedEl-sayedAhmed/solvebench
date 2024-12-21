"""
Your Order, Please
https://www.codewars.com/kata/your-order-please

Your task is to sort a given string. Each word in the string will contain a single number. This number is the position the word should have in the result.

Note: Numbers can be from 1 to 9. So 1 will be the first word (not 0).

If the input string is empty, return an empty string. The words in the input String will only contain valid consecutive numbers.

Examples:
"is2 Thi1s T4est 3a"  -->  "Thi1s is2 3a T4est"
"4of Fo1r pe6ople g3ood th5e the2"  -->  "Fo1r the2 g3ood 4of th5e pe6ople"
""  -->  ""
"""

def order(sentence):
    # words = sentence.split()
    # num_to_word = {}
    # for word in words:
    #     for char in word:
    #         if char.isdigit():
    #             num_to_word[int(char)] = word
    # num_to_word = dict(sorted(num_to_word.items()))
    # strList = list(num_to_word.values())
    # resStr = " ".join(strList)
    # return resStr
    
    # Solution 2: More optimized
    def get_number(word):
        for char in word:
            if char.isdigit():
                return int(char)
            
    words = sentence.split()
    sorted_words = sorted(words, key=get_number)
    sorted_words = " ".join(sorted_words)
    return sorted_words
                

def test_solution():
    """
    Test function with various test cases to verify the solution.
    """
    test_cases = [
        ("is2 Thi1s T4est 3a", "Thi1s is2 3a T4est"),  # Example 1
        ("4of Fo1r pe6ople g3ood th5e the2", "Fo1r the2 g3ood 4of th5e pe6ople"),  # Example 2
        ("", ""),  # Example 3
        ("3word 1word 2word", "1word 2word 3word"),  # Additional test case
        ("word1 word2 word3", "word1 word2 word3"),  # Already sorted
    ]
    
    for args, expected in test_cases:
        result = order(args)
        if result == expected:
            print(f"✅ Test Case passed")
        else:
            print(f"❌ Test Case failed")
            print(f"   Input: {args}")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}\n")

if __name__ == "__main__":
    test_solution() 