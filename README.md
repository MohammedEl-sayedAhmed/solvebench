# Problem Solving Training

This repository contains my solutions to various programming problems from different platforms like LeetCode, HackerRank, and others.

## Structure

```
├── leetcode                # Solutions to LeetCode problems
│   ├── easy                # Easy level problems
│   ├── medium              # Medium level problems
│   └── hard                # Hard level problems
├── hackerrank              # Solutions to HackerRank problems
├── AdventOfCode            # Solutions to Advent Of Code problems
└── others                  # Solutions to problems from other platforms
```

## Solutions

##### LeetCode

| #    | Title                                                                                                   | Solution                                               | Difficulty | Notes                                                     |
| ---- | ----------------------------------------------------------------------------------------------------    | ---------------------------------------------------    | ---------- | --------------------------------------------------------- |
| 1    | [Two Sum](https://leetcode.com/problems/two-sum/)                                                       | [Python](leetcode/easy/two_sum.py)                     | Easy       | Hash map approach                                         |
| 11   | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)                   | [Python](leetcode/medium/container_with_most_water.py) | Medium     | Two-pointer approach                                      |
| 15   | [3Sum](https://leetcode.com/problems/3sum/)                                                             | [Python](leetcode/medium/three_sum.py)                 | Medium     | Two-pointer approach with sorting                         |
| 20   | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)                                   | [Python](leetcode/easy/valid_parentheses.py)           | Easy       | Stack approach                                            |
| 35   | [Search Insert Position](https://leetcode.com/problems/search-insert-position/)                         | [Python](leetcode/easy/search_insert_position.py)      | Easy       | Binary Search                                             |
| 125  | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)                                     | [Python](leetcode/easy/valid_palindrome.py)            | Easy       | Two-pointer or string reverse approach                    |
| 155  | [Min Stack](https://leetcode.com/problems/min-stack/)                                                   | [Python](leetcode/medium/min_stack.py)                 | Medium     | Extra Stack to track the min value for each index         |
| 167  | [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)                           | [Python](leetcode/medium/two_sum_ii.py)                | Medium     | Two-pointer approach with sorted array                    |
| 169  | [Majority Element](https://leetcode.com/problems/majority-element/)                                     | [Python](leetcode/easy/majority_element.py)            | Easy       | Boyer-Moore Voting Algorithm                              |
| 392  | [Is Subsequence](https://leetcode.com/problems/is-subsequence/)                                         | [Python](leetcode/easy/is_subsequence.py)              | Easy       | Two-pointer approach                                      |
| 412  | [Fizz Buzz](https://leetcode.com/problems/fizz-buzz/)                                                   | [Python](leetcode/easy/fizz_buzz.py)                   | Easy       | String array based on divisibility                        |
| 888  | [Fair Candy Swap](https://leetcode.com/problems/fair-candy-swap/)                                       | [Python](leetcode/easy/fair_candy_swap.py)             | Easy       | Exchange candy boxes to equalize total                    |
| 1177 | [Can Make Palindrome from Substring](https://leetcode.com/problems/can-make-palindrome-from-substring/) | [Python](leetcode/medium/can_make_palindrome.py)       | Medium     | Frequency count and replacement strategy using Prefix Sum |

##### Codewars

| # | Title                                                                  | Solution                                 | Difficulty | Notes                                                                                                                                     |
| - | -------------------------------------------------------------------    | -------------------------------------    | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 2 | [Weight for Weight](https://www.codewars.com/kata/weight-for-weight)   | [Python](codewars/weight_for_weight.py)  | 5 kyu      | Sort numbers by the sum of their digits using lambda function                                                                             |
| 5 | [Pete, the Baker](https://www.codewars.com/kata/pete-the-baker)        | [Python](codewars/pete_the_baker.py)     | 5 kyu      | Greedy approach to calculate max number of cakes based on the limiting ingredient                                                         |
| 5 | [Count IP Addresses](https://www.codewars.com/kata/count-ip-addresses) | [Python](codewars/count_ip_addresses.py) | 5 kyu      | Converts IP addresses to integers to calculate the number of addresses between two given IPv4 addresses                                   |
| 5 | [Flatten](https://www.codewars.com/kata/flatten)                       | [Python](codewars/flatten.py)            | 5 kyu      | Recursively flattens lists and appends non-list items to the result                                                                       |
| 7 | [Your Order, Please](https://www.codewars.com/kata/your-order-please)  | [Python](codewars/your_order_please.py)  | 6 kyu      | Sort words in a string based on the number in each word, returning them in the correct order                                              |
| 5 | [Luck Check](https://www.codewars.com/kata/luck-check)                 | [Python](codewars/luck_check.py)         | 5 kyu      | Check if a ticket number is lucky by comparing sums of digits on the left and right halves, with input validation for non-numeric strings |

##### HackerRank

| Challenge                        | Solution                | Difficulty | Notes       |
| -----------------------------    | --------------------    | ---------- | ----------- |
| [Challenge Name](challenge_link) | [Python](solution_link) | Easy       | Brief notes |


##### Advent Of Code

| Challenge                                                      | Solution                                                 | Difficulty | Notes                                                                                                            | Year  | Day |
| ---                                                            | ---                                                      | ---        | ---                                                                                                              | ---   | --- |
| [Day 10: Syntax Scoring](https://adventofcode.com/2021/day/10) | [Python](AdventOfCode/2021/10/2021_10_Syntax_Scoring.py) | Medium     | Stack based approach with dicts for opening, closing, errors calculations  similar to valid parenthesis problem. | 2021  | 10  |

##### Others

| Platform    | Challenge                                                                       | Solution                                | Difficulty | Notes                                                                                   |
| ----------- | ----------------------------------------------------------------------------    | ------------------------------------    | ---------- | --------------------------------------------------------------------------------------- |
| Coding Game | [Rectangle Partition](https://www.codingame.com/ide/puzzle/rectangle-partition) | [Python](others/rectangle_partition.py) | Hard       | Brute force is not optimized, An improved version using length_freq counting dictionary |

## How to Use

1. Navigate to the specific platform folder
2. Each solution file is named according to the problem
3. Solutions include problem description and explanation in comments

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author

- **Mohammed El-sayed Ahmed**
- GitHub: [@MohammedEl-sayedAhmed](https://github.com/MohammedEl-sayedAhmed)

## Acknowledgments

- Thanks to all the coding platforms for providing great problems to solve
- Special thanks to the programming community for their continuous support

## Contact

If you have any questions or suggestions, feel free to reach out to me.

## Stats

![LeetCode Stats](https://leetcard.jacoblin.cool/MohammedElsayed?theme=nord&font=Chakra%20Petch&animation=true&ext=activity)

---

⭐ Star this repository if you find it helpful!
