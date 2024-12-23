# AOC 2024/01

Parse the input file and retrieve the two lists.

## Star 1

Sort each list so the numbers can be paired up easily by their "minimum rank", which happen to be their new index.
Sum their absolute difference to get the total distance.

## Star 2

For each number in the left list, count the number of times it appears in the right list.
If the number appears multiple times in the left list, only compute its contribution to the similarity score once.
