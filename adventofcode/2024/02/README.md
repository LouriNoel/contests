# AOC 2024/02

Parse the input file line by line and retrieve all numbers.

Each line is a _report_, which is an ordered list of _levels_.

## Star 1

Count the number of safe reports.

A report is safe if all these conditions are true:

1. The levels only ever increase or decrease
2. The (absolute) difference between a level and the next is 1, 2 or 3

Compute the difference between each adjacent levels.
These rules are equivalent when we consider the minimum and maximum difference:

1. Their multiplication is strictly positive
2. The minimum is at least -3 and the maximum is at most +3

The first rule ensures the levels are all either increasing or decreasing,
because otherwise the minimum difference would be negative and the maximum difference would be positive,
so they would not be of the same sign and their multiplication would not be positive.

Also, checking the _strict_ positiveness ensures that the minimum and maximum difference is not 0,
so no difference in the report is 0 either (so all of them are at least 1).

At last, we check the +3/-3 limit.

## Star 2

For each number in the left list, count the number of times it appears in the right list.
If the number appears multiple times in the left list, only compute its contribution to the similarity score once.
